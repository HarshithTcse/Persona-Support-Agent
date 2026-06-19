# Security FAQ

**Product:** Nimbus Cloud Platform
**Category:** Security & Compliance
**Last updated:** April 2026

## 1. Data Encryption

- **In transit:** All traffic to and from Nimbus (dashboard, API, webhooks) is encrypted using TLS 1.2 or higher. TLS 1.0/1.1 connections are rejected.
- **At rest:** Customer data is encrypted at rest using AES-256. Database-level encryption keys are rotated annually and managed through a dedicated key management service, separate from application servers.

## 2. Compliance Certifications

Nimbus maintains the following, available for review under **Settings → Security → Compliance Reports** (Enterprise plan) or upon request from Growth-plan customers under NDA:
- SOC 2 Type II (audited annually)
- GDPR compliance (EU data processing addendum available for all customers with EU users)
- CCPA compliance (California Consumer Privacy Act)

Nimbus is **not** currently HIPAA-compliant and does not offer a Business Associate Agreement (BAA) — customers in healthcare contexts handling PHI should not store such data in Nimbus.

## 3. Two-Factor Authentication (2FA)

2FA is available to all plans via authenticator app (TOTP) or SMS. Enterprise admins can enforce mandatory 2FA workspace-wide under **Settings → Security → Require 2FA**, which blocks login for any member who hasn't set it up until they do so. SMS-based 2FA is supported but authenticator-app TOTP is recommended, as SMS is more vulnerable to SIM-swapping attacks.

## 4. Password Requirements

- Minimum 10 characters, including at least one number and one symbol.
- Checked against a database of known breached passwords at signup and password-change time; matches are rejected.
- Password history: the last 5 passwords cannot be reused.
- No mandatory periodic password expiration (forced rotation) — current security guidance favors strong, unique passwords with 2FA over frequent forced changes, which tend to encourage weaker password choices.

## 5. Data Residency

Enterprise customers can choose between US and EU data hosting regions at signup. Data residency cannot be changed after initial provisioning without a full data migration, which must be scheduled with the infrastructure team and may take 1–2 weeks depending on data volume.

## 6. Data Retention & Account Deletion

- Active account data is retained indefinitely while the subscription is active.
- Upon account closure, data enters a 30-day grace period (recoverable by contacting support) before permanent deletion.
- After the 30-day grace period, data is permanently and irrecoverably deleted from production systems within 7 additional days, and from backups within 90 days (backups are retained for disaster-recovery purposes and cannot be selectively purged faster without compromising backup integrity for other customers).

## 7. Vulnerability Disclosure

Nimbus operates a responsible disclosure program. Security researchers can report vulnerabilities to security@nimbuscloud.io. Reports are acknowledged within 2 business days. Nimbus does not currently offer paid bug bounties but issues public acknowledgment (with researcher consent) for valid, responsibly disclosed findings.

## 8. Incident Response

In the event of a confirmed data breach affecting customer data, Nimbus commits to notifying affected workspace admins within 72 hours of confirmation, in line with GDPR notification requirements, including: what data was affected, likely cause, and remediation steps taken. This is separate from the general incident communication process described in `service_outage.md`, which covers availability incidents rather than data security incidents.

## 9. API Key & Credential Security

- API keys and OAuth client secrets are never displayed again after initial creation (see `integration_setup.md` Section 3) — only regeneration is offered if lost.
- Nimbus support agents can never view, retrieve, or reset a customer's API secret or password directly — all credential resets are self-service (password reset flow) or require full identity verification through Trust & Safety for account-recovery edge cases.
- Any inbound request asking Nimbus to "send my API key" or "tell me what my password is" should be treated as a potential social engineering attempt and declined regardless of how the request is justified.

## 10. Escalation Criteria

Escalate immediately (treat as high priority) when:
- A customer reports unauthorized access to their account or suspects a data breach.
- A request involves bypassing standard credential-reset or identity-verification processes.
- A vulnerability report is received through a support channel rather than security@nimbuscloud.io.
- Any request related to deleting data before the standard 30-day grace period (requires special handling per data protection regulations in some jurisdictions, e.g., GDPR "right to erasure" requests, which follow a separate verified process).
