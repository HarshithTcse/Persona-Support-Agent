# Integration Setup Guide

**Product:** Nimbus Cloud Platform
**Category:** Integrations & Connectors
**Last updated:** March 2026

## 1. Integration Methods Supported

Nimbus offers three ways to connect external tools:

1. **Native Connectors** — pre-built, one-click integrations (Salesforce, HubSpot, Shopify, Slack, Zapier) configured under **Settings → Integrations → Marketplace**.
2. **OAuth Apps (Custom)** — for developers building bespoke integrations against the Nimbus REST API.
3. **Webhooks** — outbound event notifications to a customer-hosted endpoint.

## 2. Setting Up a Native Connector (Example: Salesforce)

1. Go to **Settings → Integrations → Marketplace → Salesforce → Connect**.
2. You'll be redirected to Salesforce's login screen — sign in with an account that has API access enabled (Salesforce Professional Edition and above; Essentials Edition does not support API access and cannot be connected).
3. Approve the requested scopes (read/write Contacts, Leads, and Opportunities).
4. Choose a sync direction: **One-way (Nimbus → Salesforce)**, **One-way (Salesforce → Nimbus)**, or **Two-way sync**.
5. Map fields between systems on the field-mapping screen. Unmapped fields are not synced and will not throw errors — this is the most common cause of "my data isn't showing up" tickets.
6. Click **Activate Sync**. Initial historical sync can take 15 minutes to several hours depending on record volume (typically ~1,000 records/minute).

## 3. Setting Up a Custom OAuth App

1. Go to **Settings → Developer → OAuth Apps → Create New App**.
2. Provide an app name, redirect URI (must be HTTPS in production; `http://localhost` is permitted only in sandbox mode), and select required scopes.
3. Nimbus generates a `client_id` and `client_secret`. The secret is shown only once — store it securely (e.g., in a secrets manager), as it cannot be retrieved again and must be regenerated if lost.
4. Implement the standard OAuth 2.0 Authorization Code flow:
   - Redirect users to `https://app.nimbuscloud.io/oauth/authorize?client_id=...&redirect_uri=...&scope=...`
   - Exchange the returned `code` for tokens at `POST /oauth/token`.
5. See `token_expiration.md` for access/refresh token lifecycle details.

## 4. Setting Up Webhooks

1. Go to **Settings → Developer → Webhooks → Add Endpoint**.
2. Enter your HTTPS endpoint URL (self-signed certificates are rejected; the endpoint must present a valid CA-signed cert).
3. Select event types to subscribe to (e.g., `contact.created`, `campaign.sent`, `subscription.updated`).
4. Nimbus generates a signing secret used to compute the `X-Nimbus-Signature` HMAC header on every delivery — verify this on your endpoint to confirm payload authenticity.
5. Use the **Send Test Event** button to confirm your endpoint responds with `2xx` before relying on it in production.

See `api_troubleshooting.md` Section 6 for webhook delivery troubleshooting.

## 5. Common Setup Issues

| Symptom | Likely Cause | Fix |
|---|---|---|
| "Connection failed" during OAuth redirect | Redirect URI mismatch between app config and actual callback URL | Ensure exact match, including trailing slashes and http vs https |
| Sync completes but no records appear | Unmapped fields, or sync filter excluding records (e.g., "only sync contacts created after [date]") | Review field mapping and sync filters in connector settings |
| Salesforce connector won't connect | Salesforce edition lacks API access | Confirm Professional Edition or higher with API add-on enabled |
| Two-way sync creates duplicate records | Matching key (usually email) not configured consistently on both systems | Set the same unique matching field on both sides under sync settings |
| Webhook test event succeeds but production events never arrive | Event type subscription not actually selected, or endpoint behind auth wall that blocks Nimbus's IP range | Check subscribed event types; whitelist Nimbus's published IP ranges |

## 6. Rate Limits for Bulk Sync

Initial historical syncs and bulk imports are subject to a separate, higher rate limit pool than standard API usage (Section 3 of `api_troubleshooting.md`) to avoid disrupting real-time integrations during large backfills. Customers syncing more than 500,000 records should contact support beforehand to schedule the sync during off-peak hours.

## 7. Disconnecting an Integration

Disconnecting a native connector or OAuth app immediately revokes all associated tokens (see `token_expiration.md` Section 4) and halts syncing, but does not delete any data already synced in either direction. Re-connecting starts a fresh sync rather than resuming from where it left off, unless "Resume from last sync" is explicitly selected.

## 8. Escalation Criteria

Escalate when:
- A sync has been "in progress" for more than 4 hours with no progress movement.
- A customer reports data was overwritten or deleted as a result of a two-way sync conflict.
- Custom OAuth app review is requested for listing in the public marketplace (handled by the Partner Engineering team, not support).
