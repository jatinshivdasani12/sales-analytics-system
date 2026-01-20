# utils/data_processor.py


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region"
    ]

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect number of fields
        if len(parts) != len(headers):
            continue

        tx = dict(zip(headers, parts))

        # Handle commas within ProductName
        tx["ProductName"] = tx["ProductName"].replace(",", "").strip()

        # Convert numeric fields
        try:
            tx["Quantity"] = int(tx["Quantity"].replace(",", "").strip())
            tx["UnitPrice"] = float(tx["UnitPrice"].replace(",", "").strip())
        except ValueError:
            continue

        # Clean string fields
        tx["TransactionID"] = tx["TransactionID"].strip()
        tx["ProductID"] = tx["ProductID"].strip()
        tx["CustomerID"] = tx["CustomerID"].strip()
        tx["Region"] = tx["Region"].strip()

        transactions.append(tx)

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    Returns: tuple (valid_transactions, invalid_count, filter_summary)
    """

    valid_transactions = []
    invalid_count = 0

    available_regions = set()
    amounts = []

    for tx in transactions:
        # Required keys check
        required_keys = [
            "TransactionID", "Date", "ProductID", "ProductName",
            "Quantity", "UnitPrice", "CustomerID", "Region"
        ]
        if not all(k in tx for k in required_keys):
            invalid_count += 1
            continue

        # Region must not be empty
        if tx["Region"].strip() == "":
            invalid_count += 1
            continue

        # ID format checks
        if not tx["TransactionID"].startswith("T"):
            invalid_count += 1
            continue

        if not tx["ProductID"].startswith("P"):
            invalid_count += 1
            continue

        if not tx["CustomerID"].startswith("C"):
            invalid_count += 1
            continue

        # Value checks
        if tx["Quantity"] <= 0 or tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue

        # Amount calculation
        amount = tx["Quantity"] * tx["UnitPrice"]
        tx["Amount"] = amount

        available_regions.add(tx["Region"])
        amounts.append(amount)

        valid_transactions.append(tx)

    # Display filter options
    print("Available Regions:", sorted(list(available_regions)))

    if amounts:
        print("Transaction Amount Range (min-max):", min(amounts), "-", max(amounts))
    else:
        print("Transaction Amount Range (min-max): 0 - 0")

    # Apply filters
    filtered = valid_transactions.copy()
    filtered_by_region = 0
    filtered_by_amount = 0

    if region:
        before = len(filtered)
        filtered = [t for t in filtered if t["Region"] == region]
        filtered_by_region = before - len(filtered)
        print(f"After Region filter '{region}': {len(filtered)} records")

    if min_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["Amount"] >= min_amount]
        filtered_by_amount += before - len(filtered)
        print(f"After Min Amount filter {min_amount}: {len(filtered)} records")

    if max_amount is not None:
        before = len(filtered)
        filtered = [t for t in filtered if t["Amount"] <= max_amount]
        filtered_by_amount += before - len(filtered)
        print(f"After Max Amount filter {max_amount}: {len(filtered)} records")

    summary = {
        "total_input": len(transactions),
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(filtered)
    }

    return filtered, invalid_count, summary
