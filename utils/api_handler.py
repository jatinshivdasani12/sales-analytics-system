# utils/api_handler.py

import requests


BASE_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Requirements:
    - Fetch all available products (use limit=100)
    - Handle connection errors with try-except
    - Return empty list if API fails
    - Print status message (success/failure)
    """

    try:
        response = requests.get(f"{BASE_URL}?limit=100", timeout=10)

        if response.status_code == 200:
            data = response.json()
            products = data.get("products", [])
            print(f"✅ API Success: Fetched {len(products)} products")
            return products
        else:
            print(f"❌ API Failure: Status Code {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"❌ API Connection Error: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    Returns: dict
    """

    mapping = {}

    for product in api_products:
        pid = product.get("id")

        if pid is None:
            continue

        mapping[pid] = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating")
        }

    return mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    Saves enriched data to 'data/enriched_sales_data.txt'
    """

    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        try:
            # Extract numeric ID from ProductID (P101 -> 101)
            product_id_str = enriched_tx.get("ProductID", "").strip()
            numeric_id = int(product_id_str.replace("P", ""))

            if numeric_id in product_mapping:
                info = product_mapping[numeric_id]

                enriched_tx["API_Category"] = info.get("category")
                enriched_tx["API_Brand"] = info.get("brand")
                enriched_tx["API_Rating"] = info.get("rating")
                enriched_tx["API_Match"] = True
            else:
                enriched_tx["API_Category"] = None
                enriched_tx["API_Brand"] = None
                enriched_tx["API_Rating"] = None
                enriched_tx["API_Match"] = False

        except Exception:
            enriched_tx["API_Category"] = None
            enriched_tx["API_Brand"] = None
            enriched_tx["API_Rating"] = None
            enriched_tx["API_Match"] = False

        enriched_transactions.append(enriched_tx)

    # Save to file
    save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt")

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions back to file

    Requirements:
    - Create output file with all original + new fields
    - Use pipe delimiter
    - Handle None values appropriately
    """

    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    try:
        with open(filename, "w", encoding="utf-8") as f:
            # Write header
            f.write("|".join(headers) + "\n")

            # Write rows
            for tx in enriched_transactions:
                row = []
                for h in headers:
                    value = tx.get(h)

                    # Convert None to empty string
                    if value is None:
                        value = ""

                    row.append(str(value))

                f.write("|".join(row) + "\n")

        print(f"✅ Enriched data saved to: {filename}")

    except Exception as e:
        print(f"❌ Failed to save enriched data: {e}")
