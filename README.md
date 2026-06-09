# Silk Road Ledger

Silk Road Ledger is a small-business finance automation dashboard built with Python and Streamlit. It turns messy invoice, expense, and payment spreadsheets into clean financial insights, unpaid-invoice tracking, cashflow metrics, data-quality checks, and business summaries.

The project uses fake sample data only. It does not use paid APIs, API keys, or real company data.

## Live Demo

The deployed Streamlit app is available here:

https://silk-road-ledger.streamlit.app/

## Business Problem

Many small businesses still manage invoices, expenses, and payments manually in Excel. This often leads to repeated manual work and avoidable reporting issues:

- Customer and vendor names are typed inconsistently
- Dates appear in different formats
- Duplicate rows enter monthly reports
- Invoice IDs are missing or incorrect
- Expense categories are incomplete
- Invalid or negative amounts are not caught quickly
- Unpaid and overdue invoices are difficult to track
- Monthly cashflow reporting takes too much time

The result is a finance process that is manual, error-prone, and hard to repeat consistently.

## Solution

Silk Road Ledger automates a simple monthly finance workflow.

The application generates realistic messy sample data, cleans and validates it, matches payments to invoices, calculates key finance metrics, and presents the results in a Streamlit dashboard.

The goal is to show how a small business can move from manual spreadsheet work to a repeatable finance reporting process.

## Key Features

- Generate realistic messy invoice, expense, and payment data
- Clean and standardize raw spreadsheet data
- Validate common data-quality issues
- Match payments to invoices
- Flag unpaid and overdue invoices
- Calculate revenue, expenses, cash received, and net cashflow
- Identify top customers and vendors
- Create monthly cashflow outputs
- Generate Plotly HTML reports
- Display results in a Streamlit dashboard
- Produce a rule-based business summary

## Project Workflow

text Raw spreadsheets -> data cleaning -> validation -> finance metrics -> dashboard/report 

## Dashboard Overview

The Streamlit dashboard includes:

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
- Workflow explanation

## Project Structure

text small-business-finance-automation/ ├── data/ │   ├── raw_invoices.csv │   ├── raw_expenses.csv │   └── raw_payments.csv ├── outputs/ │   ├── clean_invoices.csv │   ├── clean_expenses.csv │   ├── clean_payments.csv │   ├── invoice_status.csv │   ├── summary_metrics.csv │   ├── monthly_cashflow.csv │   ├── data_quality_report.csv │   ├── top_customers.csv │   ├── top_vendors.csv │   ├── overdue_by_customer.csv │   ├── monthly_revenue_vs_expenses.html │   └── overdue_invoices_by_customer.html ├── src/ │   ├── generate_sample_data.py │   ├── clean_data.py │   ├── analyze_finance.py │   └── generate_report.py ├── dashboard.py ├── main.py ├── requirements.txt ├── .gitignore └── README.md 

## How to Run Locally

Create and activate a virtual environment:

bash python -m venv .venv source .venv/bin/activate 

On some machines, use python3 instead of python.

Install dependencies:

bash pip install -r requirements.txt 

Run the full automation pipeline:

bash python main.py 

Launch the Streamlit dashboard:

bash streamlit run dashboard.py 

If the streamlit command is not available directly, run:

bash python -m streamlit run dashboard.py 

## Streamlit Deployment

This project is ready for Streamlit Community Cloud.

Deployment settings:

text Repository: Aaron-cody/small-business-finance-automation Branch: main Main file path: dashboard.py 

The dashboard automatically generates sample data and output files if required files are missing, which helps the app run cleanly after deployment.

## Generated Outputs

Running python main.py creates:

- data/raw_invoices.csv
- data/raw_expenses.csv
- data/raw_payments.csv
- outputs/clean_invoices.csv
- outputs/clean_expenses.csv
- outputs/clean_payments.csv
- outputs/invoice_status.csv
- outputs/summary_metrics.csv
- outputs/monthly_cashflow.csv
- outputs/data_quality_report.csv
- outputs/top_customers.csv
- outputs/top_vendors.csv
- outputs/overdue_by_customer.csv
- outputs/monthly_revenue_vs_expenses.html
- outputs/overdue_invoices_by_customer.html

## Automation Logic

The code is intentionally simple and interview-ready:

- generate_sample_data.py creates fake messy finance CSV files.
- clean_data.py standardizes text, dates, categories, IDs, and amounts.
- analyze_finance.py calculates finance metrics and invoice status.
- generate_report.py creates Plotly HTML charts.
- main.py runs the full workflow in order.
- dashboard.py presents the results in Streamlit.

## Business Value

Silk Road Ledger demonstrates how automation can reduce manual finance administration for a small business.

Instead of repeatedly cleaning spreadsheets by hand, the business can run one workflow that:

- cleans raw finance data
- flags issues for review
- calculates key financial metrics
- highlights overdue invoices
- produces dashboard-ready outputs
- supports faster monthly reporting

## Interview Explanation

I built Silk Road Ledger as a small-business finance automation dashboard. The business case is a company that manages invoices, expenses, and payments manually in Excel. The data is messy, so the owner spends too much time cleaning spreadsheets, checking unpaid invoices, and calculating monthly cashflow.

My solution uses Python to automate that workflow. It generates realistic sample data, cleans and validates it, flags data-quality issues, matches payments to invoices, calculates cashflow and overdue invoice metrics, and displays everything in a Streamlit dashboard.

This project demonstrates practical automation, process improvement, data-quality checks, finance reporting, and business-focused thinking. It is simple enough to explain clearly, but realistic enough to show how automation can reduce manual work.

## Limitations

Current limitations:

- Uses fake sample CSV data
- Payment matching is rule-based and simple
- No user authentication
- No database
- No real accounting software integration
- No user-uploaded files yet

## Future Improvements

Possible improvements:

- Add Excel export for business users
- Add file upload for user-provided spreadsheets
- Add automated monthly email summaries
- Add unit tests for cleaning and analysis logic
- Add a database for historical monthly reporting
- Add authentication for multiple users
- Connect to accounting software or cloud storage
- Add more advanced anomaly detection for unusual invoices or expenses