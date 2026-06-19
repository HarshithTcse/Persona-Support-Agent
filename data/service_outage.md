# Service Outages, Status Communication & SLA

**Product:** Nimbus Cloud Platform
**Category:** Reliability & Incident Management
**Last updated:** April 2026

## 1. Status Page

Real-time platform status is published at **status.nimbuscloud.io**, independent of the main application infrastructure (hosted on a separate provider) so it remains reachable during a Nimbus-side outage. Users can subscribe to incident updates via email, SMS, or RSS.

## 2. Incident Severity Classification

| Severity | Definition | Example | Target Update Frequency |
|---|---|---|---|
| SEV-1 (Critical) | Full platform outage or data integrity risk affecting all customers | API and dashboard both unreachable | Every 30 minutes until resolved |
| SEV-2 (Major) | Core feature unavailable or significantly degraded for a large customer subset | Email-sending pipeline delayed by >1 hour | Every 60 minutes |
| SEV-3 (Minor) | Non-core feature degraded, workaround available | Reporting dashboard slow to load | Every 4 hours or upon resolution |
| SEV-4 (Cosmetic) | Visual/UI bug with no functional impact | Misaligned button on settings page | Resolved in next release; not posted to status page |

## 3. Service Level Agreement (SLA) — Paid Plans

| Plan | Uptime Commitment | Service Credit if Missed |
|---|---|---|
| Starter | No formal SLA | N/A |
| Growth | 99.5% monthly uptime | 10% of monthly fee credited per 0.5% below target |
| Enterprise | 99.95% monthly uptime | 25% of monthly fee credited per 0.1% below target, capped at 100% |

Uptime is calculated based on successful health-check responses from the core API and dashboard, measured at 1-minute intervals, excluding scheduled maintenance windows announced at least 72 hours in advance.

## 4. Scheduled Maintenance

Planned maintenance is announced at least 72 hours ahead via the status page and email to workspace admins. Standard maintenance windows are Sundays 02:00–04:00 UTC, chosen as the lowest-traffic period across Nimbus's global customer base. Maintenance windows are excluded from SLA uptime calculations.

## 5. What to Do During an Active Outage

For customers reporting issues during a confirmed active incident:
1. Direct them to the status page for real-time updates rather than promising a specific resolution time not yet confirmed by engineering.
2. Do not speculate on root cause before the engineering team's post-incident summary is published — incorrect speculation has historically caused customer confusion and repeat tickets.
3. Log the customer's account/workspace ID against the incident ticket so they can be proactively notified of SLA credits if applicable, without requiring them to file a separate claim.

## 6. SLA Credit Claims

Eligible customers are automatically identified and credited within one billing cycle following a SEV-1 or SEV-2 incident that breached their plan's SLA. Customers who believe they qualify but were not credited can request a manual review — this always requires escalation to the billing team along with the specific incident date/time, since automatic detection occasionally misses edge cases (e.g., customers on custom Enterprise contracts with non-standard terms).

## 7. Post-Incident Reports (PIR)

For every SEV-1 and SEV-2 incident, Nimbus publishes a Post-Incident Report within 5 business days, including: timeline, root cause, customer impact, and remediation steps taken to prevent recurrence. PIRs are posted publicly on the status page and linked from the original incident notification.

## 8. Escalation Criteria

Escalate to a human agent (do not attempt to resolve via documentation alone) when:
- A customer reports an outage that does not appear on the status page — this may indicate an issue isolated to their specific account/region rather than a platform-wide incident, and needs investigation.
- A customer disputes an SLA credit calculation.
- Data loss or data integrity concerns are raised in connection with an incident — these are always treated as high priority regardless of the incident's official severity classification.
