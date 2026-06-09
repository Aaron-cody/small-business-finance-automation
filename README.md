# Silk Road Ledger

Silk Road Ledger is a small-business finance automation dashboard built with Python and Streamlit. It helps small firms turn messy invoice, expense, and payment spreadsheets into clean financial insights, unpaid-invoice tracking, cashflow metrics, and simple business summaries.

The project uses fake sample data only. It does not use paid APIs, API keys, or real company data.

## Business Problem

Many small businesses still manage invoices, expenses, and payments manually in Excel. That process can create recurring problems:

- Customer and vendor names are typed inconsistently
- Dates appear in different formats
- Duplicate rows are copied into reports
- Invoice IDs are missing or incorrect
- Categories are incomplete
- Negative or invalid amounts are not caught quickly
- Unpaid and overdue invoices are hard to track

The owner loses time cleaning spreadsheets, checking unpaid invoices, calculating cashflow, and preparing a monthly overview.

## Solution

Silk Road Ledger automates a simple monthly finance workflow:

1. Generate realistic messy sample finance data
2. Clean and standardize the raw spreadsheet data
3. Validate common data-quality issues
4. Match payments to invoices
5. Calculate revenue, expenses, unpaid invoices, overdue invoices, and cashflow
6. Export dashboard-ready CSV and HTML reports
7. Display the results in a Streamlit dashboard

The result is a repeatable process that turns manual spreadsheet work into clean business insight.

## Project Workflow

```text
Raw spreadsheets -> data cleaning -> validation -> finance metrics -> dashboard/report
```

The dashboard includes:

- Total invoiced
- Cash received
- Expenses
- Net cashflow
- Unpaid invoices
- Overdue invoices
- Data quality issues
- Monthly cashflow charts
- Unpaid and overdue invoice tables
- Top customers and vendors
- Data-quality review
- Rule-based business summary

## Project Structure

```text
small-business-finance-automation/
├── data/
│   ├── raw_invoices.csv
│   ├── raw_expenses.csv
│   └── raw_payments.csv
├── outputs/
│   ├── clean_invoices.csv
│   ├── clean_expenses.csv
│   ├── clean_payments.csv
│   ├── summary_metrics.csv
│   ├── monthly_cashflow.csv
│   ├── data_quality_report.csv
│   └── report charts
├── src/
│   ├── generate_sample_data.py
│   ├── clean_data.py
│   ├── analyze_finance.py
│   └── generate_report.py
├── dashboard.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How to Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On some machines, use `python3` instead of `python`.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the full pipeline:

```bash
python main.py
```

Launch the Streamlit dashboard:

```bash
streamlit run dashboard.py
```

If the `streamlit` command is not available directly, run:

```bash
python -m streamlit run dashboard.py
```

## Streamlit Deployment

This project is ready for Streamlit Community Cloud.

Deployment steps:

1. Push the project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
dashboard.py
```

5. Deploy the app.

The dashboard automatically generates sample data and outputs if required files are missing, which helps the app run cleanly after deployment.

## Generated Outputs

Running `python main.py` creates:

- `data/raw_invoices.csv`
- `data/raw_expenses.csv`
- `data/raw_payments.csv`
- `outputs/clean_invoices.csv`
- `outputs/clean_expenses.csv`
- `outputs/clean_payments.csv`
- `outputs/invoice_status.csv`
- `outputs/summary_metrics.csv`
- `outputs/monthly_cashflow.csv`
- `outputs/data_quality_report.csv`
- `outputs/top_customers.csv`
- `outputs/top_vendors.csv`
- `outputs/overdue_by_customer.csv`
- `outputs/monthly_revenue_vs_expenses.html`
- `outputs/overdue_invoices_by_customer.html`

## Automation Logic

The code is intentionally simple and interview-ready:

- `generate_sample_data.py` creates fake messy finance CSV files.
- `clean_data.py` standardizes text, dates, categories, IDs, and amounts.
- `analyze_finance.py` calculates finance metrics and invoice status.
- `generate_report.py` creates Plotly HTML charts.
- `main.py` runs the full workflow in order.
- `dashboard.py` presents the results in Streamlit.

## Interview Explanation for Montis-Q

I built Silk Road Ledger as a small-business finance automation dashboard. The business case is a company that manages invoices, expenses, and payments manually in Excel. The data is messy, so the owner spends too much time cleaning spreadsheets, checking unpaid invoices, and calculating monthly cashflow.

My solution uses Python to automate that workflow. It generates realistic sample data, cleans and validates it, flags data-quality issues, matches payments to invoices, calculates cashflow and overdue invoice metrics, and displays everything in a Streamlit dashboard.

This project demonstrates practical automation, process improvement, data quality checks, finance reporting, and business-focused thinking. It is simple enough to explain clearly, but realistic enough to show how automation can reduce manual work.

## Limitations and Future Improvements

Current limitations:

- Uses fake sample CSV data
- Payment matching is rule-based and simple
- No user authentication
- No database
- No real accounting system integration

Possible improvements:

- Add Excel export for business users
- Add automated monthly email summaries
- Add unit tests for cleaning and analysis logic
- Add file upload for user-provided spreadsheets
- Add a database for historical monthly reporting
- Connect to accounting software or cloud storage
