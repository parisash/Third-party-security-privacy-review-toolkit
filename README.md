# Third-Party Security and Privacy Review Toolkit

A practical cybersecurity GRC and privacy governance project that converts vendor questionnaire responses, privacy review data and evidence records into vendor risk ratings, evidence gaps and approval recommendations.

This project demonstrates how third-party security and privacy reviews can be structured into an auditable workflow for vendor assurance, risk-based approval and stakeholder reporting.

## Project Summary

Third-party and vendor risk is a major part of cybersecurity governance. Organisations need to understand whether vendors have appropriate security controls, privacy safeguards, evidence records and contractual protections before approving or continuing the service relationship.

This project uses simulated data to demonstrate how vendor assurance can be converted into a structured and repeatable review process.

The workflow connects:

```text
Vendor Questionnaire → Privacy Review → Evidence Register → Risk Rating → Approval Recommendation
```

## Why This Project Matters

Vendor reviews are not only about collecting questionnaires. A practical review should answer:

* What service does the vendor provide?
* What type of data does the vendor access?
* Does the vendor process personal or sensitive data?
* Are core security controls in place?
* Is privacy governance evidence available?
* Are subprocessors declared?
* Is incident notification defined?
* Is evidence missing, weak or incomplete?
* Should the vendor be approved, approved with conditions or rejected until remediation?

This project demonstrates how those questions can be translated into a simple risk-based decision workflow.

## Key Features

* Vendor security questionnaire dataset
* Privacy review checklist
* Vendor evidence register
* Security and privacy control gap scoring
* Evidence quality scoring
* Missing evidence detection
* Vendor risk rating
* Approval recommendation logic
* Python-generated vendor risk register
* Executive-ready vendor assurance report

## Repository Structure

```text
third-party-security-privacy-review-toolkit/
│
├── data/
│   ├── vendor_questionnaire.csv
│   ├── privacy_review_checklist.csv
│   └── vendor_evidence_register.csv
│
├── src/
│   └── generate_vendor_risk_report.py
│
├── reports/
│   ├── vendor_risk_register.csv
│   └── vendor_executive_summary.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Input Files

### `data/vendor_questionnaire.csv`

Contains simulated vendor security questionnaire responses.

Each vendor record includes:

* Vendor name
* Service type
* Data access level
* Business criticality
* ISO 27001 status
* MFA enforcement
* Encryption at rest
* Encryption in transit
* Incident notification status
* Subprocessor declaration
* Business owner
* Review status

### `data/privacy_review_checklist.csv`

Captures privacy governance questions for each vendor.

Each record includes:

* Whether personal data is processed
* Whether sensitive data is processed
* Data minimisation review status
* Retention period status
* Data residency visibility
* DPIA requirement
* DPA requirement
* Privacy risk notes

### `data/vendor_evidence_register.csv`

Tracks vendor assurance evidence.

Each evidence record includes:

* Evidence item
* Evidence type
* Evidence status
* Evidence quality
* Review notes

This helps show whether vendor responses are supported by reviewable evidence.

## Generated Outputs

Running the Python script generates two portfolio-ready outputs.

### `reports/vendor_risk_register.csv`

A combined vendor risk register that links:

```text
Vendor Questionnaire → Privacy Review → Evidence Summary → Risk Rating → Approval Recommendation
```

It includes:

* Security and privacy control gap score
* Evidence risk score
* Evidence quality risk score
* Vendor risk score
* Risk rating
* Approval recommendation

### `reports/vendor_executive_summary.md`

An executive-style report that summarises:

* Total vendors reviewed
* Critical and high risk vendors
* Vendors with missing evidence
* Vendors processing sensitive data
* Vendor risk rating summary
* Review status summary
* Top risk vendors
* Recommended actions

## How the Risk Logic Works

The script calculates a vendor risk score using:

```text
Vendor Risk Score =
Criticality Score
+ Data Access Score
+ Security/Privacy Control Gap Score
+ Evidence Risk Score
+ Evidence Quality Risk Score
```

The project then assigns a risk rating:

```text
Critical → Do not approve until key gaps are remediated
High → Approve with conditions and remediation plan
Medium → Approve with monitoring and evidence follow-up
Low → Approve
```

## Example Workflow

```text
Vendor Questionnaire
        ↓
Privacy Review Checklist
        ↓
Evidence Register
        ↓
Python Risk Scoring Script
        ↓
Vendor Risk Register
        ↓
Executive Summary Report
```

## How to Run

Install dependencies:

```bash
py -m pip install -r requirements.txt
```

Run the report generator:

```bash
py src/generate_vendor_risk_report.py
```

Check generated reports:

```bash
dir reports
```

Expected outputs:

```text
vendor_risk_register.csv
vendor_executive_summary.md
```

## Example Governance Questions Answered

This project helps answer questions such as:

* Which vendors present the highest security and privacy risk?
* Which vendors process sensitive or personal data?
* Which vendors have missing or weak evidence?
* Which vendors require a DPA or DPIA?
* Which vendors should only be approved with conditions?
* Which vendor reviews require follow-up before approval?
* What evidence is required to support the assurance decision?

## Skills Demonstrated

This project demonstrates practical capability in:

* Cybersecurity GRC
* Third-party risk management
* Vendor security review
* Privacy governance
* DPIA/DPA-style assessment thinking
* Evidence register management
* Risk-based approval decisions
* Security and privacy control review
* Audit-readiness reporting
* Python reporting automation
* Executive risk communication

## Career Relevance

This project aligns with roles such as:

* Cybersecurity GRC Analyst
* Cybersecurity Analyst
* Information Security Analyst
* Security Governance Analyst
* Third-Party Risk Analyst
* Risk and Compliance Analyst
* Security Assurance Analyst
* Data Privacy Analyst
* Privacy Governance Analyst

## Practical Value

This project shows how third-party assurance can be made structured, traceable and repeatable.

It demonstrates the ability to:

* Interpret vendor responses
* Identify missing security and privacy evidence
* Assess privacy risk
* Link vendor data access to assurance requirements
* Assign risk ratings
* Produce approval recommendations
* Communicate vendor risk to decision-makers

## Future Improvements

Planned improvements include:

* Add Streamlit dashboard
* Add vendor risk heatmap
* Add remediation tracker
* Add vendor reassessment dates
* Add evidence expiry dates
* Add ISO 27001 and SOC 2 evidence mapping
* Add APRA CPS 234 and privacy obligation mapping
* Add Power BI-ready output
* Add sample vendor approval workflow
* Add screenshots of generated reports

## Disclaimer

This project uses simulated vendor security and privacy review data for portfolio and learning purposes. It does not contain real vendor, client, employer, security, privacy, audit or confidential organisational data.

## Author

**Parisa Shojaei**

Cybersecurity GRC · Cloud Security · Privacy Governance · Risk Analytics · AI Assurance | Turning risks into audit-ready evidence
