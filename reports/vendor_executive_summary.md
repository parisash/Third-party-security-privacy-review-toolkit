# Third-Party Security and Privacy Review Executive Summary

## Overview

This report summarises a simulated third-party security and privacy review.

The project demonstrates how vendor questionnaire responses, privacy review data and evidence records can be converted into risk ratings, evidence gaps and approval recommendations.

The workflow connects:

Vendor Questionnaire -> Privacy Review -> Evidence Register -> Vendor Risk Rating -> Approval Recommendation

## Key Metrics

| Metric | Value |
|---|---:|
| Total vendors reviewed | 8 |
| Critical risk vendors | 3 |
| High risk vendors | 1 |
| Vendors with missing evidence | 3 |
| Vendors processing sensitive data | 3 |

## Vendor Risk Rating Summary

| risk_rating   |   vendor_count |
|:--------------|---------------:|
| Critical      |              3 |
| Low           |              2 |
| Medium        |              2 |
| High          |              1 |

## Review Status Summary

| review_status            |   vendor_count |
|:-------------------------|---------------:|
| In Review                |              4 |
| Open                     |              2 |
| Approved With Conditions |              1 |
| Approved                 |              1 |

## Top Risk Vendors

| vendor_id   | vendor_name        | service_type                       | data_access_level   | criticality   |   vendor_risk_score | risk_rating   |   missing_evidence_count |   weak_evidence_count | approval_recommendation                                           |
|:------------|:-------------------|:-----------------------------------|:--------------------|:--------------|--------------------:|:--------------|-------------------------:|----------------------:|:------------------------------------------------------------------|
| V-006       | LearnHub LMS       | Learning management system         | Personal            | Medium        |                  24 | Critical      |                        2 |                     2 | Do not approve until key security and privacy gaps are remediated |
| V-008       | DataClean API      | Data processing and enrichment API | Sensitive           | Critical      |                  21 | Critical      |                        1 |                     1 | Do not approve until key security and privacy gaps are remediated |
| V-003       | QuickSurvey Pro    | Survey and feedback collection     | Personal            | Medium        |                  19 | Critical      |                        1 |                     1 | Do not approve until key security and privacy gaps are remediated |
| V-002       | PeopleTrack HR     | HR records management              | Sensitive           | Critical      |                  16 | High          |                        0 |                     1 | Approve with conditions and remediation plan                      |
| V-005       | SupportDesk Online | Customer support ticketing         | Personal            | High          |                  11 | Medium        |                        0 |                     0 | Approve with monitoring and evidence follow-up                    |

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
