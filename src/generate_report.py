"""Generate dashboard-ready Plotly HTML charts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px


OUTPUT_DIR = Path("outputs")


def generate_report() -> None:
    """Create HTML charts for monthly performance and overdue invoices."""
    monthly = pd.read_csv(OUTPUT_DIR / "monthly_cashflow.csv")
    overdue = pd.read_csv(OUTPUT_DIR / "overdue_by_customer.csv")

    monthly_long = monthly.melt(
        id_vars="month",
        value_vars=["revenue", "expenses"],
        var_name="metric",
        value_name="amount",
    )
    monthly_fig = px.bar(
        monthly_long,
        x="month",
        y="amount",
        color="metric",
        barmode="group",
        title="Monthly Revenue vs Expenses",
        labels={"month": "Month", "amount": "Amount (EUR)", "metric": "Metric"},
    )
    monthly_fig.write_html(OUTPUT_DIR / "monthly_revenue_vs_expenses.html", include_plotlyjs="cdn")

    if overdue.empty:
        overdue = pd.DataFrame({"customer_name": ["No overdue invoices"], "overdue_amount": [0]})
    overdue_fig = px.bar(
        overdue,
        x="customer_name",
        y="overdue_amount",
        title="Overdue Invoice Amount by Customer",
        labels={"customer_name": "Customer", "overdue_amount": "Overdue Amount (EUR)"},
    )
    overdue_fig.write_html(OUTPUT_DIR / "overdue_invoices_by_customer.html", include_plotlyjs="cdn")


if __name__ == "__main__":
    generate_report()
    print("HTML report charts saved in outputs/.")

