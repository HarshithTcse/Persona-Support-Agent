# Billing Policy

**Product:** Nimbus Cloud Platform
**Category:** Billing & Payments
**Last updated:** January 2026

## 1. Billing Cycles

Nimbus offers two billing cycles, selectable at signup or changeable at any time from **Settings → Billing → Plan**:
- **Monthly** — billed on the same calendar day each month as the original signup date.
- **Annual** — billed once per year; includes a 20% discount versus monthly pricing.

Switching from monthly to annual mid-cycle takes effect immediately with a prorated credit applied for unused monthly time. Switching from annual to monthly only takes effect at the end of the current annual term (no mid-term downgrades to avoid partial-refund complexity).

## 2. Accepted Payment Methods

- Credit/debit card (Visa, Mastercard, Amex, Discover)
- ACH direct debit (US workspaces on Enterprise plan only)
- Wire transfer (Enterprise plan, annual billing only, minimum $5,000/year)
- Nimbus does not accept PayPal, cryptocurrency, or postal checks.

## 3. Failed Payments

If a scheduled payment fails:
1. **Day 0:** Payment attempt fails; admin receives an email notification.
2. **Day 3:** Automatic retry #1.
3. **Day 5:** Automatic retry #2; in-app banner appears for all workspace admins.
4. **Day 7:** Final retry. If it fails, the workspace enters **Restricted Mode** (see `account_lockout.md`, Section 4).
5. **Day 67 (60 days into Restricted Mode):** Workspace data is archived. Reactivating after archival requires contacting support and may take up to 48 hours to fully restore.

## 4. Refund Policy

- **Monthly plans:** No refunds for partial months. Cancelling mid-cycle stops future billing but does not refund the current period.
- **Annual plans:** Pro-rated refund available within the first 30 days of an annual purchase or renewal ("30-day satisfaction window"). After 30 days, annual payments are non-refundable, but the subscription remains active through the paid term.
- **Billing errors:** Duplicate charges or charges processed after a confirmed cancellation are refunded in full within 5–7 business days once verified — these are not subject to the 30-day window since they are Nimbus errors, not buyer's-remorse cancellations.

## 5. Proration

Upgrading a plan mid-cycle (e.g., Growth → Enterprise) is prorated: the customer is charged the difference for the remaining days in the current billing period. Downgrading a plan does not trigger an immediate refund; the lower price takes effect at the next renewal date, and the customer retains current-tier features until then.

## 6. Adding/Removing Seats

Additional user seats are billed on a per-seat, prorated basis for the remainder of the current billing cycle, then included in the next full invoice. Removing a seat does not generate a refund for the current cycle but reduces the seat count (and cost) starting the next cycle.

## 7. Taxes

Sales tax / VAT is calculated based on the workspace's billing address country and, in the US, state. Tax-exempt organizations (e.g., registered nonprofits) can submit exemption documentation via **Settings → Billing → Tax Exemption** for review; approval typically takes 3–5 business days and is not retroactive to past invoices.

## 8. Invoices and Receipts

All invoices are available under **Settings → Billing → Invoice History** as downloadable PDFs. Invoices reflect the legal entity name and tax ID on file at the time of billing — changes to billing details do not retroactively update past invoices.

## 9. Billing Disputes — Escalation Required

The following billing scenarios must always be escalated to a human billing specialist rather than resolved via self-service guidance, per company policy:
- Any chargeback or disputed transaction with the customer's bank/card issuer.
- Requests for refunds outside the standard policy windows described above (case-by-case exceptions require manager approval).
- Suspected fraudulent charges.
- Enterprise contract-level billing terms (custom pricing, multi-year commitments, invoicing terms outside Net 30).

This is a firm policy: support agents and automated systems must not promise exceptions to refund timelines or waive fees without escalation.
