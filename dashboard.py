"""Streamlit dashboard for Silk Road Ledger."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analyze_finance import analyze_finance
from src.clean_data import clean_data
from src.generate_report import generate_report
from src.generate_sample_data import generate_sample_data


OUTPUT_DIR = Path("outputs")
APP_NAME = "Silk Road Ledger"
APP_TAGLINE = "Small Business Finance Automation"
APP_DESCRIPTION = (
    "Clean messy invoice, expense, and payment data into cashflow insights, "
    "unpaid-invoice tracking, and dashboard-ready reports."
)
APP_WORKFLOW_LINE = "From messy spreadsheets to clean finance insight in one repeatable workflow."


REQUIRED_OUTPUTS = [
    OUTPUT_DIR / "summary_metrics.csv",
    OUTPUT_DIR / "monthly_cashflow.csv",
    OUTPUT_DIR / "invoice_status.csv",
    OUTPUT_DIR / "data_quality_report.csv",
    OUTPUT_DIR / "overdue_by_customer.csv",
    OUTPUT_DIR / "top_customers.csv",
    OUTPUT_DIR / "top_vendors.csv",
    OUTPUT_DIR / "clean_expenses.csv",
    OUTPUT_DIR / "clean_payments.csv",
]


def ensure_outputs_exist() -> None:
    """Generate sample data and reports when deployed without output files."""
    if all(path.exists() for path in REQUIRED_OUTPUTS):
        return

    generate_sample_data()
    clean_data()
    analyze_finance()
    generate_report()


@st.cache_data
def load_outputs() -> dict[str, pd.DataFrame]:
    ensure_outputs_exist()
    return {
        "summary": pd.read_csv(OUTPUT_DIR / "summary_metrics.csv"),
        "monthly": pd.read_csv(OUTPUT_DIR / "monthly_cashflow.csv"),
        "invoices": pd.read_csv(OUTPUT_DIR / "invoice_status.csv", parse_dates=["invoice_date", "due_date"]),
        "quality": pd.read_csv(OUTPUT_DIR / "data_quality_report.csv"),
        "overdue": pd.read_csv(OUTPUT_DIR / "overdue_by_customer.csv"),
        "customers": pd.read_csv(OUTPUT_DIR / "top_customers.csv"),
        "vendors": pd.read_csv(OUTPUT_DIR / "top_vendors.csv"),
        "expenses": pd.read_csv(OUTPUT_DIR / "clean_expenses.csv", parse_dates=["expense_date"]),
        "payments": pd.read_csv(OUTPUT_DIR / "clean_payments.csv", parse_dates=["payment_date"]),
    }


def euro(value: float) -> str:
    return f"EUR {value:,.0f}"


def metric_value(summary: pd.DataFrame, metric: str) -> float:
    return float(summary.loc[summary["metric"] == metric, "value"].iloc[0])


def quality_issue_count(quality: pd.DataFrame, issue_types: list[str]) -> int:
    return int(quality.loc[quality["issue_type"].isin(issue_types), "issue_count"].sum())


def business_table(df: pd.DataFrame, column_names: dict[str, str]) -> pd.DataFrame:
    """Return a display-only dataframe with business-friendly column labels."""
    return df.rename(columns=column_names)


def quality_report_for_display(quality: pd.DataFrame) -> pd.DataFrame:
    issue_labels = {
        "duplicate_rows_removed": "Duplicates removed",
        "missing_invoice_ids": "Missing invoice IDs",
        "invalid_or_negative_amounts": "Invalid or negative amounts",
        "missing_categories": "Missing categories",
        "unknown_invoice_ids": "Unknown invoice IDs",
        "invalid_dates": "Invalid dates",
    }
    display = quality.copy()
    display["issue_type"] = display["issue_type"].replace(issue_labels)
    return business_table(
        display,
        {
            "dataset": "Dataset",
            "issue_type": "Issue type",
            "issue_count": "Issue count",
            "notes": "Notes",
        },
    )


def show_header() -> None:
    st.title(APP_NAME)
    st.caption(APP_TAGLINE)
    st.write(APP_DESCRIPTION)
    st.write(APP_WORKFLOW_LINE)
    st.divider()


def show_kpis(cards: list[tuple[str, str]]) -> None:
    first_row = st.columns(4)
    second_row = st.columns(3)
    columns = list(first_row) + list(second_row)

    for column, (label, value) in zip(columns, cards):
        with column.container(border=True):
            st.caption(label)
            st.subheader(value)


def show_business_summary(
    overdue_count: int,
    overdue_amount: float,
    latest_net_cashflow: float,
    largest_customer: str,
) -> None:
    st.info(
        "Business summary: "
        f"The business has {overdue_count} overdue invoices worth {euro(overdue_amount)}. "
        f"Latest monthly net cashflow is {euro(latest_net_cashflow)}. "
        f"The largest overdue customer is {largest_customer}."
    )


def build_monthly_chart(monthly: pd.DataFrame, title: str):
    metric_labels = {
        "cash_received": "Cash received",
        "expenses": "Expenses",
        "net_cashflow": "Net cashflow",
    }
    chart_data = monthly.melt(
        id_vars="month",
        value_vars=["cash_received", "expenses", "net_cashflow"],
        var_name="metric",
        value_name="amount",
    )
    chart_data["metric"] = chart_data["metric"].replace(metric_labels)
    fig = px.line(
        chart_data,
        x="month",
        y="amount",
        color="metric",
        markers=True,
        title=title,
        labels={"month": "Month", "amount": "Amount (EUR)", "metric": "Metric"},
        color_discrete_map={
            "Cash received": "#1f6f68",
            "Expenses": "#b45f2a",
            "Net cashflow": "#3f4e8c",
        },
    )
    fig.update_layout(legend_title_text="", margin=dict(l=10, r=10, t=50, b=10))
    return fig


def main() -> None:
    st.set_page_config(page_title=f"{APP_NAME} | Finance Dashboard", page_icon="SR", layout="wide")
    show_header()

    data = load_outputs()
    summary = data["summary"]
    monthly = data["monthly"].sort_values("month")
    invoices = data["invoices"]
    quality = data["quality"]
    overdue = data["overdue"]
    expenses = data["expenses"]
    payments = data["payments"]

    total_invoiced = metric_value(summary, "total_invoiced_revenue")
    total_paid = metric_value(summary, "total_amount_paid")
    total_expenses = metric_value(summary, "total_expenses")
    net_cashflow = metric_value(summary, "net_cashflow")
    unpaid_amount = metric_value(summary, "unpaid_invoice_amount")
    overdue_amount = metric_value(summary, "overdue_invoice_amount")
    overdue_count = int(metric_value(summary, "overdue_invoice_count"))
    issue_count = int(metric_value(summary, "data_quality_issues_found"))

    latest_month = monthly.iloc[-1]
    largest_customer = "No overdue customer"
    if not overdue.empty:
        largest_customer = overdue.sort_values("overdue_amount", ascending=False).iloc[0]["customer_name"]

    unpaid_invoices = invoices[invoices["is_unpaid"]].sort_values("due_date")
    overdue_invoices = invoices[invoices["is_overdue"]].sort_values("due_date")
    flagged_invoice_records = invoices[["missing_invoice_id_flag", "invalid_amount_flag", "invalid_date_flag"]].any(axis=1)
    flagged_expense_records = expenses[["missing_category_flag", "invalid_amount_flag", "invalid_date_flag"]].any(axis=1)
    flagged_payment_records = payments[
        ["missing_invoice_id_flag", "unknown_invoice_id_flag", "invalid_amount_flag", "invalid_date_flag"]
    ].any(axis=1)
    flagged_records = int(flagged_invoice_records.sum() + flagged_expense_records.sum() + flagged_payment_records.sum())
    total_clean_records = len(invoices) + len(expenses) + len(payments)
    clean_records = total_clean_records - flagged_records

    overview_tab, invoices_tab, cashflow_tab, quality_tab, workflow_tab = st.tabs(
        ["Overview", "Invoices", "Cashflow", "Data Quality", "Workflow"]
    )

    with overview_tab:
        show_kpis(
            [
                ("Total invoiced", euro(total_invoiced)),
                ("Cash received", euro(total_paid)),
                ("Expenses", euro(total_expenses)),
                ("Net cashflow", euro(net_cashflow)),
                ("Unpaid invoices", euro(unpaid_amount)),
                ("Overdue invoices", euro(overdue_amount)),
                ("Data quality issues", f"{issue_count}"),
            ]
        )
        show_business_summary(
            overdue_count=overdue_count,
            overdue_amount=overdue_amount,
            latest_net_cashflow=latest_month["net_cashflow"],
            largest_customer=largest_customer,
        )
        st.plotly_chart(
            build_monthly_chart(monthly, "Monthly Cash Received, Expenses, and Net Cashflow"),
            use_container_width=True,
        )

        left, right = st.columns(2)
        with left:
            st.subheader("Top Customers")
            st.dataframe(
                business_table(
                    data["customers"],
                    {"customer_name": "Customer", "invoiced_amount": "Invoiced amount"},
                ),
                use_container_width=True,
                hide_index=True,
            )
        with right:
            st.subheader("Top Vendors")
            st.dataframe(
                business_table(
                    data["vendors"],
                    {"vendor_name": "Vendor", "expense_amount": "Expense amount"},
                ),
                use_container_width=True,
                hide_index=True,
            )

    with invoices_tab:
        st.subheader("Unpaid Invoices")
        st.dataframe(
            business_table(
                unpaid_invoices[
                    ["invoice_id", "customer_name", "due_date", "amount", "amount_paid", "amount_unpaid", "is_overdue"]
                ],
                {
                    "invoice_id": "Invoice ID",
                    "customer_name": "Customer",
                    "due_date": "Due date",
                    "amount": "Invoice amount",
                    "amount_paid": "Amount paid",
                    "amount_unpaid": "Unpaid amount",
                    "is_overdue": "Overdue",
                },
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Overdue Invoices")
        st.dataframe(
            business_table(
                overdue_invoices[["invoice_id", "customer_name", "due_date", "amount_unpaid"]],
                {
                    "invoice_id": "Invoice ID",
                    "customer_name": "Customer",
                    "due_date": "Due date",
                    "amount_unpaid": "Unpaid amount",
                },
            ),
            use_container_width=True,
            hide_index=True,
        )

        overdue_chart_data = overdue.copy()
        if overdue_chart_data.empty:
            overdue_chart_data = pd.DataFrame({"customer_name": ["No overdue invoices"], "overdue_amount": [0]})
        overdue_fig = px.bar(
            overdue_chart_data,
            x="customer_name",
            y="overdue_amount",
            title="Overdue Amount by Customer",
            labels={"customer_name": "Customer", "overdue_amount": "Overdue Amount (EUR)"},
            color_discrete_sequence=["#b45f2a"],
        )
        overdue_fig.update_layout(margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(overdue_fig, use_container_width=True)

    with cashflow_tab:
        st.subheader("Monthly Cashflow")
        st.write(
            "This chart compares cash received from customer payments, expenses paid, and the resulting monthly net cashflow."
        )
        st.plotly_chart(build_monthly_chart(monthly, "Monthly Cashflow Trend"), use_container_width=True)
        st.dataframe(
            business_table(
                monthly,
                {
                    "month": "Month",
                    "revenue": "Revenue",
                    "expenses": "Expenses",
                    "cash_received": "Cash received",
                    "net_cashflow": "Net cashflow",
                },
            ),
            use_container_width=True,
            hide_index=True,
        )

    with quality_tab:
        st.subheader("Data Quality Review")
        quality_cards = [
            ("Duplicates removed", quality_issue_count(quality, ["duplicate_rows_removed"])),
            ("Missing invoice IDs", quality_issue_count(quality, ["missing_invoice_ids"])),
            ("Invalid or negative amounts", quality_issue_count(quality, ["invalid_or_negative_amounts"])),
            ("Missing categories", quality_issue_count(quality, ["missing_categories"])),
            ("Records flagged for review", flagged_records),
            ("Clean records", clean_records),
        ]
        quality_columns = st.columns(3)
        for index, (label, value) in enumerate(quality_cards):
            with quality_columns[index % 3].container(border=True):
                st.caption(label)
                st.subheader(str(value))

        clean_vs_flagged = pd.DataFrame(
            {
                "record_type": ["Clean records", "Flagged records"],
                "records": [clean_records, flagged_records],
            }
        )
        fig = px.bar(
            clean_vs_flagged,
            x="record_type",
            y="records",
            title="Clean Records vs Flagged Records",
            labels={"record_type": "Record Type", "records": "Records"},
            color="record_type",
            color_discrete_sequence=["#1f6f68", "#b45f2a"],
        )
        fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(quality_report_for_display(quality), use_container_width=True, hide_index=True)

    with workflow_tab:
        st.subheader("Automation Workflow")
        st.write("Raw spreadsheets → data cleaning → validation → finance metrics → dashboard/report")

        steps = [
            ("1. Raw spreadsheets", "Fake messy invoice, expense, and payment CSV files simulate manual Excel exports."),
            ("2. Data cleaning", "Names, dates, categories, duplicate rows, and numeric amounts are standardized."),
            ("3. Validation", "Missing IDs, invalid amounts, unknown invoice references, and missing categories are flagged."),
            ("4. Finance metrics", "Payments are matched to invoices and the pipeline calculates cashflow and overdue amounts."),
            ("5. Dashboard/report", "Clean files, summary CSVs, Plotly reports, and this Streamlit dashboard are produced."),
        ]
        for title, detail in steps:
            with st.container(border=True):
                st.subheader(title)
                st.write(detail)

        st.write(
            "Silk Road Ledger stays intentionally simple so each part can be explained in an interview: data generation, "
            "cleaning, validation, analysis, and reporting."
        )


if __name__ == "__main__":
    main()
