from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"

QUESTIONNAIRE_FILE = DATA_DIR / "vendor_questionnaire.csv"
PRIVACY_FILE = DATA_DIR / "privacy_review_checklist.csv"
EVIDENCE_FILE = DATA_DIR / "vendor_evidence_register.csv"

OUTPUT_REGISTER_FILE = REPORTS_DIR / "vendor_risk_register.csv"
OUTPUT_REPORT_FILE = REPORTS_DIR / "vendor_executive_summary.md"


CRITICALITY_SCORE = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
    "Critical": 4,
}

DATA_ACCESS_SCORE = {
    "Internal": 1,
    "Personal": 2,
    "Confidential": 3,
    "Sensitive": 4,
}

ANSWER_SCORE = {
    "Yes": 0,
    "No": 2,
    "Partial": 1,
}

EVIDENCE_QUALITY_SCORE = {
    "Good": 0,
    "Partial": 1,
    "Weak": 2,
}

EVIDENCE_STATUS_SCORE = {
    "Provided": 0,
    "Partial": 1,
    "Missing": 2,
}


def load_csv(file_path: Path) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(f"Required file not found: {file_path}")
    return pd.read_csv(file_path)


def validate_columns(df: pd.DataFrame, required_columns: list[str], file_name: str) -> None:
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"{file_name} is missing required columns: {', '.join(missing)}")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    questionnaire = load_csv(QUESTIONNAIRE_FILE)
    privacy = load_csv(PRIVACY_FILE)
    evidence = load_csv(EVIDENCE_FILE)

    validate_columns(
        questionnaire,
        [
            "vendor_id",
            "vendor_name",
            "service_type",
            "data_access_level",
            "criticality",
            "security_contact",
            "iso_27001_certified",
            "mfa_enforced",
            "encryption_at_rest",
            "encryption_in_transit",
            "incident_notification_defined",
            "subprocessors_declared",
            "business_owner",
            "review_status",
        ],
        "vendor_questionnaire.csv",
    )

    validate_columns(
        privacy,
        [
            "vendor_id",
            "personal_data_processed",
            "sensitive_data_processed",
            "data_minimisation_reviewed",
            "retention_period_defined",
            "data_residency_known",
            "dpia_required",
            "dpa_required",
            "privacy_risk_notes",
        ],
        "privacy_review_checklist.csv",
    )

    validate_columns(
        evidence,
        [
            "vendor_id",
            "evidence_item",
            "evidence_type",
            "evidence_status",
            "evidence_quality",
            "review_notes",
        ],
        "vendor_evidence_register.csv",
    )

    return questionnaire, privacy, evidence


def summarise_evidence(evidence: pd.DataFrame) -> pd.DataFrame:
    evidence = evidence.copy()

    evidence["evidence_status_score"] = (
        evidence["evidence_status"].map(EVIDENCE_STATUS_SCORE).fillna(1).astype(int)
    )

    evidence["evidence_quality_score"] = (
        evidence["evidence_quality"].map(EVIDENCE_QUALITY_SCORE).fillna(1).astype(int)
    )

    summary = (
        evidence.groupby("vendor_id")
        .agg(
            evidence_items=("evidence_item", "count"),
            missing_evidence_count=("evidence_status_score", lambda x: (x == 2).sum()),
            weak_evidence_count=("evidence_quality_score", lambda x: (x == 2).sum()),
            evidence_risk_score=("evidence_status_score", "sum"),
            evidence_quality_risk_score=("evidence_quality_score", "sum"),
        )
        .reset_index()
    )

    return summary


def build_vendor_risk_register(
    questionnaire: pd.DataFrame,
    privacy: pd.DataFrame,
    evidence_summary: pd.DataFrame,
) -> pd.DataFrame:
    register = questionnaire.merge(privacy, on="vendor_id", how="left")
    register = register.merge(evidence_summary, on="vendor_id", how="left")

    numeric_columns = [
        "evidence_items",
        "missing_evidence_count",
        "weak_evidence_count",
        "evidence_risk_score",
        "evidence_quality_risk_score",
    ]

    for column in numeric_columns:
        register[column] = register[column].fillna(0).astype(int)

    register["criticality_score"] = (
        register["criticality"].map(CRITICALITY_SCORE).fillna(1).astype(int)
    )

    register["data_access_score"] = (
        register["data_access_level"].map(DATA_ACCESS_SCORE).fillna(1).astype(int)
    )

    control_columns = [
        "iso_27001_certified",
        "mfa_enforced",
        "encryption_at_rest",
        "encryption_in_transit",
        "incident_notification_defined",
        "subprocessors_declared",
        "data_minimisation_reviewed",
        "retention_period_defined",
        "data_residency_known",
    ]

    for column in control_columns:
        register[f"{column}_risk"] = register[column].map(ANSWER_SCORE).fillna(1).astype(int)

    risk_columns = [f"{column}_risk" for column in control_columns]

    register["security_privacy_control_gap_score"] = register[risk_columns].sum(axis=1)

    register["vendor_risk_score"] = (
        register["criticality_score"]
        + register["data_access_score"]
        + register["security_privacy_control_gap_score"]
        + register["evidence_risk_score"]
        + register["evidence_quality_risk_score"]
    )

    register["risk_rating"] = register["vendor_risk_score"].apply(assign_risk_rating)
    register["approval_recommendation"] = register.apply(assign_approval_recommendation, axis=1)

    return register.sort_values(by="vendor_risk_score", ascending=False)


def assign_risk_rating(score: int) -> str:
    if score >= 18:
        return "Critical"
    if score >= 13:
        return "High"
    if score >= 8:
        return "Medium"
    return "Low"


def assign_approval_recommendation(row: pd.Series) -> str:
    if row["risk_rating"] == "Critical":
        return "Do not approve until key security and privacy gaps are remediated"
    if row["risk_rating"] == "High":
        return "Approve with conditions and remediation plan"
    if row["risk_rating"] == "Medium":
        return "Approve with monitoring and evidence follow-up"
    return "Approve"


def markdown_table(df: pd.DataFrame, columns: list[str]) -> str:
    if df.empty:
        return "No records found."
    return df[columns].to_markdown(index=False)


def generate_report(register: pd.DataFrame) -> str:
    total_vendors = register["vendor_id"].nunique()
    critical_vendors = register[register["risk_rating"] == "Critical"]["vendor_id"].nunique()
    high_vendors = register[register["risk_rating"] == "High"]["vendor_id"].nunique()
    vendors_with_missing_evidence = register[
        register["missing_evidence_count"] > 0
    ]["vendor_id"].nunique()
    vendors_processing_sensitive_data = register[
        register["sensitive_data_processed"] == "Yes"
    ]["vendor_id"].nunique()

    risk_summary = (
        register.groupby("risk_rating")["vendor_id"]
        .nunique()
        .reset_index(name="vendor_count")
        .sort_values(by="vendor_count", ascending=False)
    )

    review_status_summary = (
        register.groupby("review_status")["vendor_id"]
        .nunique()
        .reset_index(name="vendor_count")
        .sort_values(by="vendor_count", ascending=False)
    )

    top_risk_vendors = register.head(5)

    report = f"""# Third-Party Security and Privacy Review Executive Summary

## Overview

This report summarises a simulated third-party security and privacy review.

The project demonstrates how vendor questionnaire responses, privacy review data and evidence records can be converted into risk ratings, evidence gaps and approval recommendations.

The workflow connects:

Vendor Questionnaire -> Privacy Review -> Evidence Register -> Vendor Risk Rating -> Approval Recommendation

## Key Metrics

| Metric | Value |
|---|---:|
| Total vendors reviewed | {total_vendors} |
| Critical risk vendors | {critical_vendors} |
| High risk vendors | {high_vendors} |
| Vendors with missing evidence | {vendors_with_missing_evidence} |
| Vendors processing sensitive data | {vendors_processing_sensitive_data} |

## Vendor Risk Rating Summary

{markdown_table(risk_summary, ["risk_rating", "vendor_count"])}

## Review Status Summary

{markdown_table(review_status_summary, ["review_status", "vendor_count"])}

## Top Risk Vendors

{markdown_table(
        top_risk_vendors,
        [
            "vendor_id",
            "vendor_name",
            "service_type",
            "data_access_level",
            "criticality",
            "vendor_risk_score",
            "risk_rating",
            "missing_evidence_count",
            "weak_evidence_count",
            "approval_recommendation",
        ],
    )}

## GRC and Privacy Interpretation

The highest-risk vendors are those that process sensitive or confidential data, support critical services, have incomplete security controls, weak privacy evidence or missing evidence records.

Vendors with missing incident notification procedures, unclear data residency, missing retention evidence or incomplete encryption evidence require stronger assurance before approval.

## Recommended Actions

1. Do not approve Critical risk vendors until key gaps are remediated.
2. Approve High risk vendors only with documented conditions and remediation owners.
3. Request missing evidence for vendors processing sensitive or personal data.
4. Confirm DPA and DPIA requirements before onboarding vendors with privacy risk.
5. Track vendor remediation actions through to closure evidence.
6. Reassess vendors after evidence updates or material service changes.

## Disclaimer

This report is generated from simulated vendor security and privacy review data for portfolio and learning purposes. It does not contain real vendor, client, employer, privacy, security or confidential organisational data.
"""
    return report


def save_outputs(register: pd.DataFrame, report: str) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    register.to_csv(OUTPUT_REGISTER_FILE, index=False)
    OUTPUT_REPORT_FILE.write_text(report, encoding="utf-8")

    print("Vendor security and privacy review report generated successfully.")
    print(f"- {OUTPUT_REGISTER_FILE}")
    print(f"- {OUTPUT_REPORT_FILE}")


def main() -> None:
    questionnaire, privacy, evidence = load_data()
    evidence_summary = summarise_evidence(evidence)
    register = build_vendor_risk_register(questionnaire, privacy, evidence_summary)
    report = generate_report(register)
    save_outputs(register, report)


if __name__ == "__main__":
    main()
