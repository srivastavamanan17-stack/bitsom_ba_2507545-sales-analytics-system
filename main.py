from utils.file_handler import read_sales_file
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)
from utils.report_generator import generate_sales_report


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # [1/10] Read file
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_file("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # [2/10] Parse
        print("\n[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(parsed)} records")

        # [3/10] Filter options
        regions = sorted(set(t["Region"] for t in parsed if "Region" in t))
        amounts = [
            int(t["Quantity"]) * float(t["UnitPrice"])
            for t in parsed
            if "Quantity" in t and "UnitPrice" in t
        ]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        if amounts:
            print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amt = None
        max_amt = None

        if apply_filter == "y":
            region_filter = input("Enter region (or press Enter to skip): ").strip()
            if region_filter == "":
                region_filter = None

            min_val = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_val = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amt = float(min_val) if min_val else None
            max_amt = float(max_val) if max_val else None

        # [4/10] Validate
        print("\n[4/10] Validating transactions...")
        cleaned, invalid_count, summary = validate_and_filter(
            parsed,
            region=region_filter,
            min_amount=min_amt,
            max_amount=max_amt
        )
        print(f"✓ Valid: {len(cleaned)} | Invalid: {invalid_count}")

        # [5/10] Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(cleaned)
        region_wise_sales(cleaned)
        top_selling_products(cleaned)
        customer_analysis(cleaned)
        daily_sales_trend(cleaned)
        find_peak_sales_day(cleaned)
        low_performing_products(cleaned)
        print("✓ Analysis complete")

        # [6/10] API
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # [7/10] Enrichment
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched = enrich_sales_data(cleaned, product_mapping)

        enriched_count = sum(1 for t in enriched if t.get("API_Match"))
        success_rate = (enriched_count / len(enriched)) * 100 if enriched else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched)} transactions ({success_rate:.1f}%)")

        # [8/10] Save enriched data
        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to: data/enriched_sales_data.txt")

        # [9/10] Report
        print("\n[9/10] Generating report...")
        generate_sales_report(cleaned, enriched)
        print("✓ Report saved to: output/sales_report.txt")

        # [10/10] Done
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\nERROR OCCURRED")
        print("Something went wrong while running the system.")
        print("Details:", e)


if __name__ == "__main__":
    main()
