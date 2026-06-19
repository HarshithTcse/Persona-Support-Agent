# Account Lockout: Causes, Resolution, and Prevention

**Product:** Nimbus Cloud Platform
**Category:** Account & Access
**Last updated:** February 2026

## 1. What Triggers an Account Lockout

Nimbus automatically locks an account under any of the following conditions:

1. **Repeated failed login attempts** — 5 consecutive failed password attempts within 15 minutes locks the account for 30 minutes.
2. **Suspicious login pattern** — Logins detected from a new country combined with a new device fingerprint within a short window trigger an automatic security hold, separate from the failed-attempt lock.
3. **Failed payment on a paid plan** — If a subscription invoice fails to collect after 3 retry attempts over 7 days, the workspace is moved to **Restricted Mode** (read-only access) rather than a full lockout — admin users can still log in to update billing details.
4. **Admin-initiated lock** — A workspace owner or admin can manually lock a specific user's seat from **Settings → Team → Members**.
5. **Compliance/legal hold** — Rare; applied by the Trust & Safety team pending investigation of a Terms of Service violation report. These require human review and cannot be self-resolved.

## 2. Self-Service Unlock (Failed Login Lock)

For the standard 5-failed-attempt lock:
- The lock automatically clears after 30 minutes — no action needed.
- To unlock immediately, use **Forgot Password** on the login screen (see `password_reset_guide.pdf`). A successful password reset clears the lock instantly.

## 3. Security Hold (Unusual Login Location/Device)

When this triggers, the user receives an email titled "New sign-in detected — confirm it was you" with a one-time confirmation link valid for 1 hour.
- Clicking **"Yes, this was me"** lifts the hold immediately.
- Clicking **"This wasn't me"** locks the account fully, forces a password reset, and revokes all active sessions and API tokens for that user.
- If the email is not received within 5 minutes, check spam/junk and confirm the recovery email on file is correct (recovery email can only be viewed/changed by a workspace admin if the user is locked out).

## 4. Restricted Mode (Billing-Related)

Restricted Mode is **not** a security lockout — it is a billing state. Symptoms:
- Non-admin users see a banner: "This workspace is in restricted mode. Contact your admin."
- API requests return `402 PAYMENT_REQUIRED`.
- Data is preserved and not deleted; full access resumes within 5–10 minutes of successful payment.

Workspaces remaining in Restricted Mode for more than 60 days are subject to data archival per the Billing Policy (see `billing_policy.md`).

## 5. When Self-Service Won't Work

Escalate to a human agent if:
- The user has been locked out for more than 24 hours despite a successful password reset.
- The "confirm it was you" email was never delivered after 3 resend attempts and the recovery email is confirmed correct (possible deliverability/spam-filter issue requiring backend log review).
- The lockout is flagged as a compliance/legal hold (support agents cannot lift these — must route to Trust & Safety).
- Multiple users at the same company report simultaneous lockouts, which may indicate an organization-wide SSO misconfiguration rather than individual account issues.

## 6. Prevention Recommendations

- Enable two-factor authentication (2FA) — accounts with 2FA enabled are 6x less likely to trigger suspicious-login holds because the system has a stronger trust signal.
- Use a password manager to avoid repeated failed attempts from typos.
- Keep workspace billing contact information and backup payment methods up to date to avoid Restricted Mode.
- For teams using Single Sign-On (SSO), ensure the Identity Provider (IdP) session timeout is configured to avoid users being silently logged out and then triggering failed-attempt locks when re-authenticating manually.

## 7. Data Retention During Lockout

No data is deleted during any lockout state, including security holds and Restricted Mode. Full data deletion only occurs after the account closure process outlined in the Security FAQ (`security_faq.md`), which requires explicit confirmation and a 30-day grace period.
