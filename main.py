from utils.file_handler import read_sales_data
from utils.data_processor import parse_transactions, validate_and_filter

from utils.analytics import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)

from utils.api_handler import fetch_all_products, create_product_mapping, enrich_sales_data
from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function (Task 5.1)
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()

        # [1/10] Reading data
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions\n")

        # [2/10] Parsing data
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        # [3/10] Filter options
        print("[3/10] Filter Options Available:")

        # Show available regions + amount range using validate_and_filter (without applying filters)
        valid_preview, invalid_preview, summary_preview = validate_and_filter(transactions)

        available_regions = sorted(list(set([t["Region"] for t in valid_preview])))
        amounts = [t["Amount"] for t in valid_preview] if valid_preview else []

        print("Regions:", ", ".join(available_regions))
        if amounts:
            print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")
        else:
            print("Amount Range: ₹0 - ₹0")

        user_choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount_filter = None
        max_amount_filter = None

        if user_choice == "y":
            region_filter = input("Enter region (or leave blank for all): ").strip()
            if region_filter == "":
                region_filter = None

            min_val = input("Enter minimum amount (or leave blank): ").strip()
            max_val = input("Enter maximum amount (or leave blank): ").strip()

            if min_val != "":
                min_amount_filter = float(min_val)

            if max_val != "":
                max_amount_filter = float(max_val)

            print("\nApplying filters...\n")
        else:
            print("\nNo filters applied.\n")

        # [4/10] Validating and filtering
        print("[4/10] Validating transactions...")
        valid_transactions, invalid_count, filter_summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amount_filter,
            max_amount=max_amount_filter
        )
        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}\n")

        # [5/10] Analytics
        print("[5/10] Analyzing sales data...")

        total_rev = calculate_total_revenue(valid_transactions)
        region_stats = region_wise_sales(valid_transactions)
        top_products = top_selling_products(valid_transactions, n=5)
        customer_stats = customer_analysis(valid_transactions)
        daily_trend = daily_sales_trend(valid_transactions)
        peak_day = find_peak_sales_day(valid_transactions)
        low_products = low_performing_products(valid_transactions, threshold=10)

        print("✓ Analysis complete\n")

        # [6/10] API Fetch
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # [7/10] Enrich data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)

        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match") is True)
        total_valid = len(enriched_transactions)
        success_rate = (enriched_count / total_valid * 100) if total_valid > 0 else 0.0

        print(f"✓ Enriched {enriched_count}/{total_valid} transactions ({success_rate:.1f}%)\n")

        # [8/10] Save enriched (already saved inside function but we show message)
        print("[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # [9/10] Generate report
        print("[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions, output_file="output/sales_report.txt")
        print("✓ Report saved to: output/sales_report.txt\n")

        # [10/10] Done
        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ Something went wrong.")
        print("Error:", str(e))
        print("Please check your files and try again.\n")


if __name__ == "__main__":
    main()
