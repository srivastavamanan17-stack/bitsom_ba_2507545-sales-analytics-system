from datetime import datetime
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file="output/sales_report.txt"
):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_txns = len(transactions)
    avg_order_value = total_revenue / total_txns if total_txns else 0

    dates = [t["Date"] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}" if dates else "N/A"

    region_data = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, 5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_count = sum(1 for t in enriched_transactions if t.get("API_Match"))
    failed_products = {
        t["ProductName"] for t in enriched_transactions if not t.get("API_Match")
    }
    success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 55 + "\n")
        f.write("SALES ANALYTICS REPORT\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Records Processed: {total_txns}\n")
        f.write("=" * 55 + "\n\n")


        f.write("OVERALL SUMMARY\n")
        f.write("-" * 55 + "\n")
        f.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions: {total_txns}\n")
        f.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range: {date_range}\n\n")

   
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Region':<10}{'Sales':>15}{'% of Total':>15}{'Txns':>10}\n")
        for region, data in region_data.items():
            f.write(
                f"{region:<10}₹{data['total_sales']:>14,.0f}"
                f"{data['percentage']:>14.2f}%{data['transaction_count']:>10}\n"
            )
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Rank':<6}{'Product':<20}{'Qty':>8}{'Revenue':>15}\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            f.write(f"{i:<6}{name:<20}{qty:>8}₹{rev:>14,.0f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Rank':<6}{'Customer':<15}{'Spent':>15}{'Orders':>10}\n")
        for i, (cid, data) in enumerate(list(customers.items())[:5], 1):
            f.write(
                f"{i:<6}{cid:<15}₹{data['total_spent']:>14,.0f}"
                f"{data['purchase_count']:>10}\n"
            )
        f.write("\n")


        f.write("DAILY SALES TREND\n")
        f.write("-" * 55 + "\n")
        f.write(f"{'Date':<12}{'Revenue':>15}{'Txns':>10}{'Customers':>12}\n")
        for date, data in daily_trend.items():
            f.write(
                f"{date:<12}₹{data['revenue']:>14,.0f}"
                f"{data['transaction_count']:>10}"
                f"{data['unique_customers']:>12}\n"
            )
        f.write("\n")

      
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("-" * 55 + "\n")
        f.write(f"Best Selling Day: {peak_day[0]} "
                f"(₹{peak_day[1]:,.0f}, {peak_day[2]} transactions)\n")

        if low_products:
            f.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                f.write(f" - {name} (Qty: {qty}, Revenue: ₹{rev:,.0f})\n")
        else:
            f.write("Low Performing Products: None\n")
        f.write("\n")


        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 55 + "\n")
        f.write(f"Products Enriched: {enriched_count}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Failed Products:\n")
        for p in failed_products:
            f.write(f" - {p}\n")

    print(f"Sales report generated at {output_file}")
