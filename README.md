# sales-analytics-system
Sales Data Analytics System - Python Assignment
# Sales Analytics System (Python)

This project is a **Sales Data Analytics System** built in Python.  
It reads and cleans sales transaction data, performs analytics, integrates product details using an API (DummyJSON), enriches the dataset, and generates a final sales report.

---

## 📂 Project Structure

sales-analytics-system/
│── main.py
│── requirements.txt
│── README.md
│
├── data/
│ ├── sales_data.txt
│ ├── enriched_sales_data.txt (generated)
│
├── output/
│ ├── sales_report.txt (generated)
│
└── utils/
├── file_handler.py
├── data_processor.py
├── analytics.py
├── api_handler.py
├── report_generator.py

---

## ✅ Features

- Reads sales data with encoding handling (`utf-8`, `latin-1`, `cp1252`)
- Parses and cleans messy pipe-delimited data
- Validates transactions and removes invalid records
- Optional region/amount filtering (interactive)
- Performs analytics:
  - Total Revenue
  - Region-wise sales
  - Top-selling products
  - Customer purchase analysis
  - Daily sales trend & peak sales day
  - Low-performing products
- Fetches product data from DummyJSON API
- Enriches sales data and saves output file
- Generates a comprehensive report in text format

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/sales-analytics-system.git
cd sales-analytics-system
2️⃣ Install dependencies
pip install -r requirements.txt
▶️ How to Run the Project
python main.py
You will be asked if you want to filter the data:
Example:
Do you want to filter data? (y/n):
📄 Output Files Generated
After successful execution, the system generates:
✅ Enriched Sales Data:
data/enriched_sales_data.txt
✅ Final Sales Report:
output/sales_report.txt
🌐 API Used

DummyJSON Products API
Base URL: https://dummyjson.com/products
✅ Notes

This system handles invalid transactions such as:

Missing CustomerID or Region

Quantity <= 0

UnitPrice <= 0

TransactionID not starting with 'T'

Enrichment matches ProductID like P101 → 101 with API IDs.
