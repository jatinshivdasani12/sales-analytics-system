# utils/report_generator.py

from datetime import datetime
from utils.analytics import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def format_money(amount, currency="₹"):
    try:
        return f"{currency}{amount:,.2f}"
    except Exception:
        return f"{currency}0.00"


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    # BASIC METRICS
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records_processed = len(transactions)

    total_revenue = calculate_total_revenue(transactions)
    total_transactions = len(transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0.0

    dates = [t["Date"] for t in transactions] if transactions else []
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    # REGION STATS
    region_stats = region_wise_sales(transactions)

    # TOP PRODUCTS
    top_products = top_selling_products(transactions, n=5)

    # TOP CUSTOMERS
    customer_stats = customer_analysis(transactions)
    top_customers_list = list(customer_stats.items())[:5]

    # DAILY TREND
    daily_trend = daily_sales_trend(transactions)

    # PRODUCT PERFORMANCE
    peak_day, peak_revenue, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions, threshold=10)

    # Average transaction value per region
    avg_tx_value_region = {}
    for region, stats in region_stats.items():
        tx_count = stats["transaction_count"]
        avg_tx_value_region[region] = stats["total_sales"] / tx_count if tx_count > 0 else 0.0

    # API ENRICHMENT SUMMARY
    total_enriched = 0
    failed_products = set()

    for tx in enriched_transactions:
        if tx.get("API_Match") is True:
            total_enriched += 1
        else:
            failed_products.add(tx.get("ProductName", "Unknown"))

    success_rate = (total_enriched / len(enriched_transactions) * 100) if enriched_transactions else 0.0

    # WRITE REPORT
    with open(output_file, "w", encoding="utf-8") as f:
        # 1) HEADER
        f.write("=" * 44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {now}\n")
        f.write(f"         Records Processed: {total_records_processed}\n")
        f.write("=" * 44 + "\n\n")

        # 2) OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        {format_money(total_revenue)}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  {format_money(avg_order_value)}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # 3) REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Region':<10}{'Sales':<15}{'% of Total':<12}{'Transactions'}\n")

        for region, stats in region_stats.items():
            sales = format_money(stats["total_sales"])
            pct = f"{stats['percentage']:.2f}%"
            tx_count = stats["transaction_count"]
            f.write(f"{region:<10}{sales:<15}{pct:<12}{tx_count}\n")

        f.write("\n")

        # 4) TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Product Name':<20}{'Qty Sold':<10}{'Revenue'}\n")

        for i, (name, qty, revenue) in enumerate(top_products, start=1):
            f.write(f"{i:<6}{name:<20}{qty:<10}{format_money(revenue)}\n")

        f.write("\n")

        # 5) TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Rank':<6}{'Customer ID':<15}{'Total Spent':<15}{'Orders'}\n")

        for i, (cust_id, stats) in enumerate(top_customers_list, start=1):
            f.write(f"{i:<6}{cust_id:<15}{format_money(stats['total_spent']):<15}{stats['purchase_count']}\n")

        f.write("\n")

        # 6) DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        f.write(f"{'Date':<12}{'Revenue':<15}{'Txns':<8}{'Unique Customers'}\n")

        for date, stats in daily_trend.items():
            f.write(
                f"{date:<12}{format_money(stats['revenue']):<15}{stats['transaction_count']:<8}{stats['unique_customers']}\n"
            )

        f.write("\n")

        # 7) PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 44 + "\n")
        f.write(f"Peak Sales Day: {peak_day} | Revenue: {format_money(peak_revenue)} | Transactions: {peak_count}\n\n")

        f.write("Low Performing Products (Quantity < 10)\n")
        if len(low_products) == 0:
            f.write("None\n")
        else:
            f.write(f"{'Product Name':<20}{'Qty Sold':<10}{'Revenue'}\n")
            for name, qty, revenue in low_products:
                f.write(f"{name:<20}{qty:<10}{format_money(revenue)}\n")

        f.write("\nAverage Transaction Value by Region\n")
        f.write(f"{'Region':<10}{'Avg Transaction Value'}\n")
        for region, avg_val in avg_tx_value_region.items():
            f.write(f"{region:<10}{format_money(avg_val)}\n")

        f.write("\n")

        # 8) API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total products enriched: {total_enriched}\n")
        f.write(f"Success rate: {success_rate:.2f}%\n\n")

        f.write("Products that couldn't be enriched:\n")
        if len(failed_products) == 0:
            f.write("None\n")
        else:
            for p in sorted(list(failed_products)):
                f.write(f"- {p}\n")

    print(f"✅ Report generated successfully: {output_file}")
