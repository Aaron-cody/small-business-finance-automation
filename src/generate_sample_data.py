"""Create fake messy finance data for a small business.

The generated data intentionally includes common spreadsheet problems:
duplicates, inconsistent names, missing IDs, invalid amounts, and mixed date
formats. This makes the cleaning and analysis steps realistic without using
real company data.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")


def generate_sample_data() -> None:
    """Generate raw invoice, expense, and payment CSV files."""
    DATA_DIR.mkdir(exist_ok=True)

    invoices = pd.DataFrame(
        [
            ["INV-1001", "Acme Retail", "2026-01-05", "2026-02-04", 2400, "Paid"],
            ["INV-1002", " blue sky cafe ", "01/18/2026", "02/17/2026", 1800, "paid"],
            ["INV-1003", "Northwind Studio", "2026/02/03", "2026/03/05", 3200, "Unpaid"],
            ["INV-1004", "ACME retail", "2026-02-15", "2026-03-17", 1500, "Paid"],
            ["", "Green Garden Co", "03-01-2026", "03-31-2026", 950, "Unpaid"],
            ["INV-1006", "Blue Sky Cafe", "2026-03-12", "2026-04-11", -300, "Unpaid"],
            ["INV-1007", "Summit Events", "2026-04-02", "2026-05-02", 4100, "Paid"],
            ["INV-1008", "northwind studio ", "2026-04-20", "2026-05-20", 2750, "Unpaid"],
            ["INV-1009", "Green Garden Co", "2026-05-01", "2026-05-31", 1200, "Overdue"],
            ["INV-1010", "Bright Books", "05/16/2026", "06/15/2026", 2200, "Unpaid"],
            ["INV-1011", "Acme Retail", "2026-05-22", "2026-06-21", 1750, "Paid"],
            ["INV-1012", "Summit Events", "2026-06-01", "2026-07-01", 3650, "Unpaid"],
            ["INV-1007", "Summit Events", "2026-04-02", "2026-05-02", 4100, "Paid"],
        ],
        columns=["invoice_id", "customer_name", "invoice_date", "due_date", "amount", "status"],
    )

    expenses = pd.DataFrame(
        [
            ["EXP-2001", "Office Depot", "2026-01-07", "office supplies", 260],
            ["EXP-2002", " CloudHost ", "01/15/2026", "software", 120],
            ["EXP-2003", "city utilities", "2026/02/04", "Utilities", 410],
            ["EXP-2004", "Office Depot", "2026-02-18", "Office Supplies", 180],
            ["EXP-2005", "Freelance Design Co", "03-03-2026", "", 900],
            ["EXP-2006", "Cloudhost", "2026-03-15", "Software", 120],
            ["EXP-2007", "Metro Ads", "2026-04-01", "marketing", 750],
            ["EXP-2008", "City Utilities", "2026-04-05", "utilities", -80],
            ["EXP-2009", "Freelance Design Co", "2026-05-09", "contractors", 1100],
            ["EXP-2010", "Metro Ads", "05/20/2026", "Marketing", 600],
            ["EXP-2011", "CloudHost", "2026-06-01", None, 130],
            ["EXP-2007", "Metro Ads", "2026-04-01", "marketing", 750],
        ],
        columns=["expense_id", "vendor_name", "expense_date", "category", "amount"],
    )

    payments = pd.DataFrame(
        [
            ["PAY-3001", "INV-1001", "2026-01-29", 2400],
            ["PAY-3002", "INV-1002", "02/20/2026", 1800],
            ["PAY-3003", "INV-1004", "2026-03-10", 1500],
            ["PAY-3004", "INV-1007", "2026-05-06", 4100],
            ["PAY-3005", "INV-1011", "2026-06-03", 1750],
            ["PAY-3006", "", "2026-03-30", 500],
            ["PAY-3007", "INV-9999", "2026-04-15", 250],
            ["PAY-3008", "INV-1008", "2026-06-05", -200],
            ["PAY-3004", "INV-1007", "2026-05-06", 4100],
        ],
        columns=["payment_id", "invoice_id", "payment_date", "amount_paid"],
    )

    invoices.to_csv(DATA_DIR / "raw_invoices.csv", index=False)
    expenses.to_csv(DATA_DIR / "raw_expenses.csv", index=False)
    payments.to_csv(DATA_DIR / "raw_payments.csv", index=False)


if __name__ == "__main__":
    generate_sample_data()
    print("Sample raw finance data generated in data/.")

