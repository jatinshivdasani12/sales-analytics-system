# utils/analytics.py


def calculate_total_revenue(transactions):
    total_revenue = 0.0
    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]
    return total_revenue


def region_wise_sales(transactions):
    region_stats = {}
    total_sales_all = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_stats:
            region_stats[region] = {"total_sales": 0.0, "transaction_count": 0}

        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1

    for region in region_stats:
        if total_sales_all > 0:
            region_stats[region]["percentage"] = round(
                (region_stats[region]["total_sales"] / total_sales_all) * 100, 2
            )
        else:
            region_stats[region]["percentage"] = 0.0

    sorted_regions = sorted(
        region_stats.items(), key=lambda x: x[1]["total_sales"], reverse=True
    )

    return dict(sorted_regions)


def top_selling_products(transactions, n=5):
    product_stats = {}

    for tx in transactions:
        product = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {"quantity": 0, "revenue": 0.0}

        product_stats[product]["quantity"] += qty
        product_stats[product]["revenue"] += revenue

    sorted_products = sorted(
        product_stats.items(), key=lambda x: x[1]["quantity"], reverse=True
    )

    result = []
    for product, stats in sorted_products[:n]:
        result.append((product, stats["quantity"], round(stats["revenue"], 2)))

    return result


def customer_analysis(transactions):
    customers = {}

    for tx in transactions:
        customer_id = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        product = tx["ProductName"]

        if customer_id not in customers:
            customers[customer_id] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customers[customer_id]["total_spent"] += amount
        customers[customer_id]["purchase_count"] += 1
        customers[customer_id]["products_bought"].add(product)

    for customer_id in customers:
        purchase_count = customers[customer_id]["purchase_count"]
        total_spent = customers[customer_id]["total_spent"]

        if purchase_count > 0:
            customers[customer_id]["avg_order_value"] = round(total_spent / purchase_count, 2)
        else:
            customers[customer_id]["avg_order_value"] = 0.0

        customers[customer_id]["products_bought"] = sorted(list(customers[customer_id]["products_bought"]))
        customers[customer_id]["total_spent"] = round(customers[customer_id]["total_spent"], 2)

    sorted_customers = sorted(
        customers.items(), key=lambda x: x[1]["total_spent"], reverse=True
    )

    return dict(sorted_customers)


def daily_sales_trend(transactions):
    daily = {}

    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        customer_id = tx["CustomerID"]

        if date not in daily:
            daily[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "unique_customers": set()
            }

        daily[date]["revenue"] += amount
        daily[date]["transaction_count"] += 1
        daily[date]["unique_customers"].add(customer_id)

    for date in daily:
        daily[date]["revenue"] = round(daily[date]["revenue"], 2)
        daily[date]["unique_customers"] = len(daily[date]["unique_customers"])

    return dict(sorted(daily.items(), key=lambda x: x[0]))


def find_peak_sales_day(transactions):
    trend = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = -1
    peak_count = 0

    for date, stats in trend.items():
        if stats["revenue"] > peak_revenue:
            peak_revenue = stats["revenue"]
            peak_date = date
            peak_count = stats["transaction_count"]

    return (peak_date, peak_revenue, peak_count)


def low_performing_products(transactions, threshold=10):
    product_stats = {}

    for tx in transactions:
        product = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if product not in product_stats:
            product_stats[product] = {"quantity": 0, "revenue": 0.0}

        product_stats[product]["quantity"] += qty
        product_stats[product]["revenue"] += revenue

    low_products = []
    for product, stats in product_stats.items():
        if stats["quantity"] < threshold:
            low_products.append((product, stats["quantity"], round(stats["revenue"], 2)))

    low_products.sort(key=lambda x: x[1])

    return low_products
