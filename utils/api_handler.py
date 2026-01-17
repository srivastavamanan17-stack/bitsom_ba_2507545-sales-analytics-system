import requests


BASE_URL = "https://dummyjson.com/products"

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns:
        list of product dictionaries
    """
    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print("Successfully fetched products from API")
        return products

    except Exception as e:
        print(f"Failed to fetch products from API: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Returns:
        dictionary mapping product IDs to info
    """
    product_mapping = {}

    for product in api_products:
        try:
            product_mapping[product["id"]] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating"),
            }
        except Exception:
            continue

    return product_mapping
def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched = []

    for t in transactions:
        enriched_txn = t.copy()

        try:
            numeric_id = int("".join(filter(str.isdigit, t["ProductID"])))

            if numeric_id in product_mapping:
                api_data = product_mapping[numeric_id]

                enriched_txn["API_Category"] = api_data.get("category")
                enriched_txn["API_Brand"] = api_data.get("brand")
                enriched_txn["API_Rating"] = api_data.get("rating")
                enriched_txn["API_Match"] = True
            else:
                enriched_txn["API_Category"] = None
                enriched_txn["API_Brand"] = None
                enriched_txn["API_Rating"] = None
                enriched_txn["API_Match"] = False

        except Exception:
            enriched_txn["API_Category"] = None
            enriched_txn["API_Brand"] = None
            enriched_txn["API_Rating"] = None
            enriched_txn["API_Match"] = False

        enriched.append(enriched_txn)

    return enriched

def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file
    """
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as file:
        file.write("|".join(headers) + "\n")

        for t in enriched_transactions:
            row = [
                str(t.get("TransactionID", "")),
                str(t.get("Date", "")),
                str(t.get("ProductID", "")),
                str(t.get("ProductName", "")),
                str(t.get("Quantity", "")),
                str(t.get("UnitPrice", "")),
                str(t.get("CustomerID", "")),
                str(t.get("Region", "")),
                str(t.get("API_Category", "")),
                str(t.get("API_Brand", "")),
                str(t.get("API_Rating", "")),
                str(t.get("API_Match", ""))
            ]
            file.write("|".join(row) + "\n")

    print(f"Enriched sales data saved to {filename}")
