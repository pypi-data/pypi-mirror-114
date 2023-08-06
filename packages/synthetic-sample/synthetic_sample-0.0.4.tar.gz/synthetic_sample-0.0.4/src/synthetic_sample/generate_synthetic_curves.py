import pandas as pd
from datetime import datetime, timedelta
from typing import Union

from src.synthetic_sample import sample_curve
from src.synthetic_sample.sample_curve import SampleCurve, CustomSampleCurve


def create_yearly_metadata_dict(period_definition: Union[tuple, list], annual_sales: int) -> dict:
    """ Creates dictionary containing each year and the total number of sales to attribute

    Args:
        period_definition: defines the time period to use
            if a tuple, expected to contain (start_date, end_date)
            if a list, expected to contain each requested year as an integer

    Returns:
        dictionary with metadata around the sales for each year. Keys are:
            start_date: first day to include for the year
            end_date: last day to include for the year
            sales: total number of sales for the year
    """
    if type(period_definition) == list:
        year_metadata_dict = {
            year: {}
            for year in period_definition
        }
    elif type(period_definition) == tuple:
        start_date = period_definition[0]
        end_date = period_definition[1]
        year_metadata_dict = {
            year: {
                "start_date": datetime(year, 1, 1),
                "end_date": datetime(year, 12, 31)
            }
            for year in range(start_date.year, end_date.year + 1)
        }
        year_metadata_dict[start_date.year]["start_date"] = pd.to_datetime(start_date)
        year_metadata_dict[end_date.year]["end_date"] = pd.to_datetime(end_date)
    else:
        raise NotImplementedError()

    for year in year_metadata_dict:
        year_dict = year_metadata_dict.get(year)
        if year_dict.get("start_date") is not None:
            start_date = year_dict["start_date"]
            end_date = year_dict["end_date"]
        else:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
        days_of_year = (end_date - start_date)
        multiplier = days_of_year / (datetime(year, 12, 31) - datetime(year, 1, 1))
        year_dict["sales"] = multiplier * annual_sales

    return year_metadata_dict


def apply_curve_to_time_period(curve: CustomSampleCurve, period_definition: Union[tuple, list],
                               seasonal_distribution: dict, annual_sales: int, annual_growth_rate: float, curve_modifiers: list) -> pd.DataFrame:
    """ Given a curve and input parameters, apply the curve to the period to create the aggregated synthetic data

    Args:
        curve: CustomSampleCurve object to apply to the year
        period_definition: defines the tim eperiod to use
            if a tuple, expected to contain (start_date, end_date)
            if a list, expected to contain each requested year as an integer
        seasonal_distribution: dictionary indicating redistribution of output according to seasonal trends
        annual_sales: annual sales for the period
        annual_growth_rate: average annual growth rate (10% growth being 1.1)

    Returns:
        dataframe with the total number of sales for each period in the requested time period
    """
    yearly_metadata_dict = create_yearly_metadata_dict(period_definition, annual_sales)
    sales_df = curve.apply(yearly_metadata_dict, seasonal_distribution, curve_modifiers)

    if type(period_definition) == tuple:
        start_date = period_definition[0] - timedelta(days=(period_definition[0].weekday() + 1))
        end_date = period_definition[1] - timedelta(days=(period_definition[1].weekday() + 1))
        start_mask = sales_df[SampleCurve.period_column_name] >= start_date
        end_mask = sales_df[SampleCurve.period_column_name] <= end_date
        sales_df = sales_df[start_mask & end_mask]

    return sales_df.reset_index(drop=True)


def generate_synthetic_curves(period_type: sample_curve.PeriodType, period_definition: Union[tuple, list],
                              annual_growth_factor: float, curve_definition: dict, seasonal_distribution: dict,
                              annual_sales: int, packages_per_sale: float, quantity_per_sale: float, curve_modifiers: list) -> pd.DataFrame:
    """ Generates synthetic sales data for given json input

    Args:
        period_type: type of period to create aggregated data for
        period_definition: definition for the period, either a list of years or a tuple of (start_date, end_date)
        annual_growth_factor: average annual growth rate (10% growth being 1.1)
        curve_definition: dictionary to define the sales curve in terms of the cumulative percentage at the end of each period
        seasonal_distribution: dictionary indicating redistribution of output according to seasonal trends
        annual_sales: annual sales for the period
        packages_per_sale: average number of packages per sale
        quantity_per_sale: average quantity sold per sale

    Returns:
        dataframe with the total number of sales, packages, and quantity for each period in the requested time period
    """
    # Create synthetic sales curve
    custom_curve = sample_curve.CustomSampleCurve(period_type, curve_definition)
    sales_time_series_df = apply_curve_to_time_period(custom_curve, period_definition, seasonal_distribution,
                                                      annual_sales, annual_growth_factor, curve_modifiers)
    sales_time_series_df.rename(columns={SampleCurve.value_column_name: "sales"}, inplace=True)

    # Add derived values based on ratio
    sales_time_series_df["packages"] = (sales_time_series_df["sales"] * packages_per_sale).apply(int)
    sales_time_series_df["quantity"] = (sales_time_series_df["sales"] * quantity_per_sale).apply(int)

    return sales_time_series_df
