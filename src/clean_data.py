"""Clean and validate raw finance CSV files."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
REPORT_COLUMNS = ["dataset", "issue_type", "issue_count", "notes"]


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def _clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype("string").str.strip()
    return df


def _title_case(series: pd.Series) -> pd.Series:
    return series.astype("string").str.replace(r"\s+", " ", regex=True).str.title()


def _parse_dates(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors="coerce", format="mixed")
    return df


def _to_number(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    df = df.copy()
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def _add_issue(report_rows: list[dict[str, object]], dataset: str, issue_type: str, count: int, notes: str) -> None:
    report_rows.append(
        {
            "dataset": dataset,
            "issue_type": issue_type,
            "issue_count": int(count),
            "notes": notes,
        }
    )


def clean_data() -> None:
    """Clean raw files and write cleaned CSVs plus a data-quality report."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    quality_rows: list[dict[str, object]] = []

    invoices = _standardize_columns(pd.read_csv(DATA_DIR / "raw_invoices.csv"))
    invoices = _clean_text_columns(invoices)
    duplicate_count = invoices.duplicated().sum()
    invoices = invoices.drop_duplicates()
    invoices["customer_name"] = _title_case(invoices["customer_name"])
    invoices["status"] = _title_case(invoices["status"]).fillna("Unknown")
    invoices = _parse_dates(invoices, ["invoice_date", "due_date"])
    invoices = _to_number(invoices, ["amount"])
    invoices["missing_invoice_id_flag"] = invoices["invoice_id"].isna() | (invoices["invoice_id"] == "")
    invoices["invalid_amount_flag"] = invoices["amount"].isna() | (invoices["amount"] <= 0)
    invoices["invalid_date_flag"] = invoices[["invoice_date", "due_date"]].isna().any(axis=1)
    invoices["amount"] = invoices["amount"].fillna(0)

    _add_issue(quality_rows, "invoices", "duplicate_rows_removed", duplicate_count, "Exact duplicate invoice rows removed.")
    _add_issue(quality_rows, "invoices", "missing_invoice_ids", invoices["missing_invoice_id_flag"].sum(), "Invoices without an ID need manual follow-up.")
    _add_issue(quality_rows, "invoices", "invalid_or_negative_amounts", invoices["invalid_amount_flag"].sum(), "Amounts must be positive numbers.")
    _add_issue(quality_rows, "invoices", "invalid_dates", invoices["invalid_date_flag"].sum(), "Invoice and due dates must parse correctly.")

    expenses = _standardize_columns(pd.read_csv(DATA_DIR / "raw_expenses.csv"))
    expenses = _clean_text_columns(expenses)
    duplicate_count = expenses.duplicated().sum()
    expenses = expenses.drop_duplicates()
    expenses["vendor_name"] = _title_case(expenses["vendor_name"])
    expenses["category"] = _title_case(expenses["category"]).fillna("Uncategorized")
    expenses.loc[expenses["category"].isin(["", "<NA>"]), "category"] = "Uncategorized"
    expenses = _parse_dates(expenses, ["expense_date"])
    expenses = _to_number(expenses, ["amount"])
    expenses["missing_category_flag"] = expenses["category"].eq("Uncategorized")
    expenses["invalid_amount_flag"] = expenses["amount"].isna() | (expenses["amount"] <= 0)
    expenses["invalid_date_flag"] = expenses["expense_date"].isna()
    expenses["amount"] = expenses["amount"].fillna(0)

    _add_issue(quality_rows, "expenses", "duplicate_rows_removed", duplicate_count, "Exact duplicate expense rows removed.")
    _add_issue(quality_rows, "expenses", "missing_categories", expenses["missing_category_flag"].sum(), "Missing categories set to Uncategorized.")
    _add_issue(quality_rows, "expenses", "invalid_or_negative_amounts", expenses["invalid_amount_flag"].sum(), "Amounts must be positive numbers.")
    _add_issue(quality_rows, "expenses", "invalid_dates", expenses["invalid_date_flag"].sum(), "Expense dates must parse correctly.")

    payments = _standardize_columns(pd.read_csv(DATA_DIR / "raw_payments.csv"))
    payments = _clean_text_columns(payments)
    duplicate_count = payments.duplicated().sum()
    payments = payments.drop_duplicates()
    payments = _parse_dates(payments, ["payment_date"])
    payments = _to_number(payments, ["amount_paid"])
    payments["missing_invoice_id_flag"] = payments["invoice_id"].isna() | (payments["invoice_id"] == "")
    payments["invalid_amount_flag"] = payments["amount_paid"].isna() | (payments["amount_paid"] <= 0)
    payments["invalid_date_flag"] = payments["payment_date"].isna()
    payments["amount_paid"] = payments["amount_paid"].fillna(0)
    known_invoice_ids = set(invoices.loc[~invoices["missing_invoice_id_flag"], "invoice_id"])
    payments["unknown_invoice_id_flag"] = ~payments["invoice_id"].isin(known_invoice_ids)

    _add_issue(quality_rows, "payments", "duplicate_rows_removed", duplicate_count, "Exact duplicate payment rows removed.")
    _add_issue(quality_rows, "payments", "missing_invoice_ids", payments["missing_invoice_id_flag"].sum(), "Payments without invoice IDs cannot be matched.")
    _add_issue(quality_rows, "payments", "unknown_invoice_ids", payments["unknown_invoice_id_flag"].sum(), "Payments linked to invoice IDs not found in invoice data.")
    _add_issue(quality_rows, "payments", "invalid_or_negative_amounts", payments["invalid_amount_flag"].sum(), "Paid amounts must be positive numbers.")
    _add_issue(quality_rows, "payments", "invalid_dates", payments["invalid_date_flag"].sum(), "Payment dates must parse correctly.")

    invoices.to_csv(OUTPUT_DIR / "clean_invoices.csv", index=False)
    expenses.to_csv(OUTPUT_DIR / "clean_expenses.csv", index=False)
    payments.to_csv(OUTPUT_DIR / "clean_payments.csv", index=False)
    pd.DataFrame(quality_rows, columns=REPORT_COLUMNS).to_csv(OUTPUT_DIR / "data_quality_report.csv", index=False)


if __name__ == "__main__":
    clean_data()
    print("Cleaned finance data saved in outputs/.")

