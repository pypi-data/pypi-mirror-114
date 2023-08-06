import argparse
import json
import pandas as pd
from pathlib import Path

from src.synthetic_sample import calculation_utils, generate_synthetic_curves, generate_synthetic_records, sample_curve

module_path = Path(__file__).parent

def run_synthetic_sample(input_dict: dict, output_directory: str, create_records_dataset: bool = False) -> dict:
    """ Main executable to create synthetic sales data based on annual curves

    Args:
        input_filepath: filepath of the request parameters in JSON format
        output_directory: filepath of the directory to save out all data to
        create_records_dataset: indicates if the individual sales records should also be created

    """
    # Unpack request dictionary to initialize variable
    default_type = input_dict.get("default_type")
    year_list = input_dict.get("year_list")
    start_date = input_dict.get("start_date")
    end_date = input_dict.get("end_date")
    total_sales = input_dict.get("total_sales")
    total_packages = input_dict.get("total_packages")
    total_quantity = input_dict.get("total_quantity")
    annual_sales = input_dict.get("annual_sales")
    annual_packages = input_dict.get("annual_packages")
    annual_quantity = input_dict.get("annual_quantity")
    annual_growth_factor = input_dict.get("annual_growth_factor")
    period_type = input_dict.get("period_type")
    curve_definition = input_dict.get("curve_definition")
    product_distribution = input_dict.get("product_distribution")
    week_distribution = input_dict.get("week_distribution")
    weekday_distribution = input_dict.get("weekday_distribution")
    seasonal_distribution = input_dict.get("seasonal_distribution")
    modifiers_list = input_dict.get("modifiers")

    # Initialize defaults and apply to inputs if necessary
    with open(f"{module_path}/defaults/lib/standard.json", "r") as f:
        default_dict = json.load(f)
    if default_type is not None:
        with open(f"{module_path}/defaults/lib/{default_type}.json", "r") as f:
            default_dict.update(json.load(f))

    if year_list is None:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        period_definition = (start_date, end_date)
    else:
        period_definition = year_list
    if annual_growth_factor is None:
        annual_growth_factor = default_dict.get("annual_growth_factor")
    if annual_sales is None:
        annual_sales = calculation_utils.get_annualized_integer(start_date, end_date, total_sales)
    if annual_packages is None:
        annual_packages = calculation_utils.get_annualized_integer(start_date, end_date, total_packages)
    if annual_quantity is None:
        annual_quantity = calculation_utils.get_annualized_integer(start_date, end_date, total_quantity)
    if product_distribution is None:
        product_distribution = default_dict.get("sku_distribution")
    if week_distribution is None:
        week_distribution = default_dict.get("week_distribution")
    if weekday_distribution is None:
        weekday_distribution = default_dict.get("weekday_distribution")
    if type(curve_definition) == str:
        with open(f"{module_path}/defaults/curves/{period_type}/{curve_definition}.json", "r") as f:
            curve_definition = json.load(f)
    if modifiers_list is None:
        modifiers_list = []

    # Preprocessing of variables
    period_type = sample_curve.PeriodType(period_type)
    # Create required ratios based on whatever inputs are provided
    annual_sales, packages_per_sale, quantity_per_sale = calculation_utils.get_sales_ratios(default_dict.get("packages_per_sale"),
                                                                                            default_dict.get("quantity_per_package"),
                                                                                            annual_sales,
                                                                                            annual_packages,
                                                                                            annual_quantity)
    # Distributions must be normalized to add up to a total of 1.0
    product_distribution = calculation_utils.normalize_dist_dict(product_distribution)
    weekday_distribution = calculation_utils.normalize_dist_dict(weekday_distribution)
    seasonal_distribution = calculation_utils.normalize_dist_dict(seasonal_distribution)

    # Generate a dataframe with sample curves and save to a csv
    sample_curves_df = generate_synthetic_curves.generate_synthetic_curves(period_type, period_definition,
                                                                           annual_growth_factor, curve_definition,
                                                                           seasonal_distribution, annual_sales,
                                                                           packages_per_sale, quantity_per_sale,
                                                                           modifiers_list)
    #sample_curves_df.to_csv(f"{output_directory}/sample_curves.csv", index=False)

    # If indicated that records should be created, run create_records_dataset() and save the result to a csv
    if create_records_dataset:
        sample_records_df = generate_synthetic_records.generate_synthetic_records(sample_curves_df, packages_per_sale,
                                                                                  quantity_per_sale,
                                                                                  week_distribution,
                                                                                  weekday_distribution,
                                                                                  product_distribution)
        if type(period_definition) == tuple:
            mask = sample_records_df["date"] <= end_date
            mask = mask & (sample_records_df["date"] >= start_date)
            sample_records_df = sample_records_df[mask]
    #    sample_records_df.to_csv(f"{output_directory}/sample_records.csv", index=False)

    return {"curve": sample_curves_df, "records": sample_records_df}


if __name__ == "__main__":
    # Create parser for cmdline args
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_filepath')
    parser.add_argument('--output_directory')
    parser.add_argument('--create_records', default=False, action='store_true')

    # Parse out cmdline args and use to run main()
    args = parser.parse_args()
    json_filepath = args.json_filepath
    output_directory = args.output_directory
    create_records = args.create_records

    # Read in input parameters
    with open(json_filepath) as f:
        input_dict = json.load(f)

    run_synthetic_sample(input_dict, output_directory, create_records)
