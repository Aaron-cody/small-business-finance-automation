"""Calculate small-business finance metrics from cleaned data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


OUTPUT_DIR = Path("outputs")
AS_OF_DATE = pd.Timestamp("2026-06-09")


def _load_clean_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    invoices = pd.read_csv(OUTPUT_DIR / "clean_invoices.csv", parse_dates=["invoice_date", "due_date"])
    expenses = pd.read_csv(OUTPUT_DIR / "clean_expenses.csv", parse_dates=["expense_date"])
    payments = pd.read_csv(OUTPUT_DIR / "clean_payments.csv", parse_dates=["payment_date"])
    return invoices, expenses, payments


def analyze_finance() -> None:
    """Create summary metrics, monthly cashflow, and grouped insight files."""
    invoices, expenses, payments = _load_clean_data()
    quality = pd.read_csv(OUTPUT_DIR / "data_quality_report.csv")

    valid_invoices = invoices[~invoices["invalid_amount_flag"]].copy()
    valid_expenses = expenses[~expenses["invalid_amount_flag"]].copy()
    valid_payments = payments[~payments["invalid_amount_flag"] & ~payments["missing_invoice_id_flag"]].copy()

    invoice_payments = valid_payments.groupby("invoice_id", as_index=False)["amount_paid"].sum()
    invoice_status = valid_invoices.merge(invoice_payments, on="invoice_id", how="left")
    invoice_status["amount_paid"] = invoice_status["amount_paid"].fillna(0)
    invoice_status["amount_unpaid"] = (invoice_status["amount"] - invoice_status["amount_paid"]).clip(lower=0)
    invoice_status["is_unpaid"] = invoice_status["amount_unpaid"] > 0
    invoice_status["is_overdue"] = invoice_status["is_unpaid"] & (invoice_status["due_date"] < AS_OF_DATE)
    invoice_status.to_csv(OUTPUT_DIR / "invoice_status.csv", index=False)

    total_invoiced = valid_invoices["amount"].sum()
    total_expenses = valid_expenses["amount"].sum()
    total_paid = valid_payments["amount_paid"].sum()
    unpaid_amount = invoice_status["amount_unpaid"].sum()
    overdue_amount = invoice_status.loc[invoice_status["is_overdue"], "amount_unpaid"].sum()
    net_cashflow = total_paid - total_expenses
    issue_count = quality["issue_count"].sum()

    summary = pd.DataFrame(
        [
            ["total_invoiced_revenue", total_invoiced],
            ["total_expenses", total_expenses],
            ["total_amount_paid", total_paid],
            ["unpaid_invoice_amount", unpaid_amount],
            ["overdue_invoice_amount", overdue_amount],
            ["net_cashflow", net_cashflow],
            ["open_invoice_count", int(invoice_status["is_unpaid"].sum())],
            ["overdue_invoice_count", int(invoice_status["is_overdue"].sum())],
            ["data_quality_issues_found", int(issue_count)],
        ],
        columns=["metric", "value"],
    )
    summary.to_csv(OUTPUT_DIR / "summary_metrics.csv", index=False)

    monthly_revenue = (
        valid_invoices.assign(month=valid_invoices["invoice_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "revenue"})
    )
    monthly_expenses = (
        valid_expenses.assign(month=valid_expenses["expense_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "expenses"})
    )
    monthly_cash = (
        valid_payments.assign(month=valid_payments["payment_date"].dt.to_period("M").astype(str))
        .groupby("month", as_index=False)["amount_paid"]
        .sum()
        .rename(columns={"amount_paid": "cash_received"})
    )
    monthly = monthly_revenue.merge(monthly_expenses, on="month", how="outer").merge(monthly_cash, on="month", how="outer")
    monthly = monthly.fillna(0).sort_values("month")
    monthly["net_cashflow"] = monthly["cash_received"] - monthly["expenses"]
    monthly.to_csv(OUTPUT_DIR / "monthly_cashflow.csv", index=False)

    top_customers = (
        valid_invoices.groupby("customer_name", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .rename(columns={"amount": "invoiced_amount"})
    )
    top_customers.to_csv(OUTPUT_DIR / "top_customers.csv", index=False)

    top_vendors = (
        valid_expenses.groupby("vendor_name", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .rename(columns={"amount": "expense_amount"})
    )
    top_vendors.to_csv(OUTPUT_DIR / "top_vendors.csv", index=False)

    overdue_by_customer = (
        invoice_status[invoice_status["is_overdue"]]
        .groupby("customer_name", as_index=False)
        .agg(overdue_amount=("amount_unpaid", "sum"), overdue_invoices=("invoice_id", "count"))
        .sort_values("overdue_amount", ascending=False)
    )
    overdue_by_customer.to_csv(OUTPUT_DIR / "overdue_by_customer.csv", index=False)


if __name__ == "__main__":
    analyze_finance()
    print("Finance analysis outputs saved in outputs/.")

