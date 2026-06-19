# Subscription Plans & Features

**Product:** Nimbus Cloud Platform
**Category:** Plans & Pricing
**Last updated:** January 2026

## 1. Plan Tiers

| Feature | Starter | Growth | Enterprise |
|---|---|---|---|
| Price (monthly billing) | $29/mo | $99/mo | Custom |
| Price (annual billing) | $23/mo (billed yearly) | $79/mo (billed yearly) | Custom |
| Included seats | 3 | 10 | Custom |
| Contacts limit | 2,500 | 50,000 | Unlimited |
| API rate limit | 60 req/min | 300 req/min | 1,200 req/min |
| Native integrations | Limited (5) | All standard connectors | All connectors + custom integration support |
| Custom roles | No | No | Yes |
| SSO (SAML/OIDC) | No | No | Yes |
| SLA | None | 99.5% uptime | 99.95% uptime |
| Support channel | Email (48h response) | Email + chat (24h response) | Dedicated CSM + priority support (4h response) |
| Audit logs | 7 days | 90 days | 2 years |

## 2. Upgrading Plans

Upgrades take effect immediately upon confirmation. The price difference for the remaining days in the current billing cycle is charged immediately (prorated); the new plan's full price applies starting the next billing cycle. All features of the new tier are unlocked instantly — there is no waiting period.

## 3. Downgrading Plans

Downgrades take effect at the **end** of the current billing cycle, not immediately — this prevents customers from losing access to data or features mid-cycle that they've already paid for. If a downgrade would put the account over a new limit (e.g., 60,000 contacts on a plan that only allows 50,000), the system blocks the downgrade and prompts the customer to first reduce usage below the new tier's limit.

## 4. Add-Ons

Available regardless of base plan tier (Growth and Enterprise only, except where noted):

| Add-On | Price | Available On |
|---|---|---|
| Additional contacts (10,000 block) | $20/mo | Growth, Enterprise |
| Additional seats | $15/seat/mo | Growth, Enterprise |
| Dedicated IP for email sending | $50/mo | Growth, Enterprise |
| SCIM auto-provisioning | $200/mo | Enterprise only |
| Extended audit log retention (beyond 2 years) | Custom | Enterprise only |

## 5. Free Trial

New workspaces receive a 14-day free trial of the Growth plan automatically, no credit card required to start. At the end of the trial:
- If no payment method is added, the workspace automatically downgrades to Starter (data is preserved; any usage exceeding Starter limits is frozen, not deleted, until upgraded again).
- Trial extensions are occasionally granted (max one 14-day extension per workspace) and must be requested via support — there is no self-service trial extension button, to prevent abuse.

## 6. Annual Plan Commitment

Annual plans lock in pricing and feature tier for the full 12-month term. Mid-term tier changes are allowed (upgrades immediately, downgrades at renewal — same logic as Section 2–3), but switching from annual to monthly billing is not permitted mid-term (see `billing_policy.md` Section 1).

## 7. Nonprofit & Education Discounts

Verified 501(c)(3) nonprofits and accredited educational institutions are eligible for a 30% discount on Growth and Enterprise plans. Verification requires submitting documentation via **Settings → Billing → Discount Eligibility** and is reviewed within 5 business days; discounts are not retroactive to prior invoices.

## 8. Plan-Related Escalations

Escalate to a human agent when:
- A customer requests a custom Enterprise quote (pricing is negotiated, not published).
- A downgrade is blocked due to usage limits and the customer disputes which records should be considered "over the limit" (e.g., disputes about duplicate or test contacts).
- A trial extension is requested for a second time.
- A nonprofit/education discount application is rejected and the customer wants to appeal.
