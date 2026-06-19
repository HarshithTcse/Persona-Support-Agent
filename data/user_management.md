# User Management & Roles

**Product:** Nimbus Cloud Platform
**Category:** Account Administration
**Last updated:** March 2026

## 1. Roles Overview

Nimbus workspaces support four built-in roles. Permissions are additive and cannot be granted individually outside these presets on Starter and Growth plans; Enterprise plans support custom roles (Section 5).

| Role | Can View Data | Can Edit Data | Can Manage Billing | Can Manage Users | Can Manage API Keys |
|---|---|---|---|---|---|
| Owner | Yes | Yes | Yes | Yes | Yes |
| Admin | Yes | Yes | No | Yes | Yes |
| Editor | Yes | Yes | No | No | No |
| Viewer | Yes | No | No | No | No |

Every workspace must have exactly one Owner. Ownership can be transferred from **Settings → Team → Transfer Ownership**, which requires the current Owner to confirm via email.

## 2. Inviting Users

Admins and Owners can invite new users from **Settings → Team → Invite Member** by entering an email address and selecting a role. Invitations:
- Are valid for 7 days, after which they expire and must be resent.
- Count against the workspace's seat limit immediately upon being sent (a pending invite occupies a seat just like an active member, to prevent seat-limit gaming).
- Can be resent or revoked at any time before acceptance.

## 3. Seat Limits by Plan

| Plan | Included Seats | Additional Seat Cost |
|---|---|---|
| Starter | 3 | Not available — must upgrade to Growth |
| Growth | 10 | $15/seat/month |
| Enterprise | Custom (negotiated) | Custom pricing |

Attempting to invite beyond the seat limit on Starter returns an in-app prompt to upgrade; Growth and Enterprise workspaces are billed automatically for additional seats per the proration rules in `billing_policy.md`.

## 4. Removing or Deactivating Users

- **Deactivate:** Removes login access and revokes all active sessions/tokens immediately, but preserves the user's historical activity attribution (e.g., "created by [Name]" remains visible). Deactivated seats can be reactivated by re-inviting the same email without losing history.
- **Delete:** Permanently anonymizes the user's identity in historical records (replaced with "Deleted User"). This action is irreversible and requires the Owner role specifically (not just Admin).

Removing a user does **not** delete content they created (contacts, campaigns, reports) — ownership of that content automatically transfers to the workspace Owner.

## 5. Custom Roles (Enterprise Only)

Enterprise workspaces can define custom roles with granular permissions across 12 permission categories (contacts, campaigns, reports, integrations, billing, users, API keys, automations, templates, deliverability settings, audit logs, and data exports). Custom roles are managed under **Settings → Team → Custom Roles** and require at least one active Enterprise contract seat to configure.

## 6. Single Sign-On (SSO) and User Provisioning

Enterprise customers can enable SAML 2.0 or OIDC SSO. With SSO enabled:
- Users are provisioned automatically on first login if "Just-in-Time Provisioning" is enabled, with role assigned based on IdP group mapping configured by the customer's IT admin.
- Without JIT provisioning, users must still be manually invited first (Section 2), and SSO only handles the authentication step, not account creation.
- SCIM-based automated deprovisioning (auto-deactivating users removed from the IdP) is available as an add-on for Enterprise customers.

## 7. Common Support Scenarios

- **"I can't invite anyone" on Starter plan:** Check if the 3-seat limit has been reached; this is the most frequent cause and resolves with an upgrade.
- **"My team member can't see the billing page":** Expected behavior for Editor/Viewer/Admin roles — only Owners can access billing (Section 1). This is not a bug.
- **"I removed someone and lost their reports":** Reports are not deleted; ownership transfers to the workspace Owner per Section 4. Direct the customer to filter reports by "All Owners" rather than their personal view.

## 8. Escalation Criteria

Escalate when:
- A customer needs an Owner transfer but the current Owner is unreachable (e.g., former employee) — this requires identity verification by the Trust & Safety team and cannot be self-served.
- SCIM provisioning errors are reported (these require backend log inspection).
- A customer disputes seat billing after a deactivation/reactivation cycle.
