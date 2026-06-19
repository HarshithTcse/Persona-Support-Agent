# API Troubleshooting Guide

**Product:** Nimbus Cloud Platform
**Audience:** Developers integrating with the Nimbus REST API
**Last updated:** March 2026

## 1. Overview

The Nimbus API (`api.nimbuscloud.io/v2`) is a REST API secured with OAuth 2.0 bearer tokens. This guide covers the most common integration failures reported to support, along with diagnostic steps and fixes.

## 2. Authentication Failures

### 2.1 Error: `401 UNAUTHORIZED` — `invalid_token`
This occurs when:
- The access token has expired (access tokens are valid for 60 minutes).
- The token was revoked because the associated API key was rotated.
- The `Authorization` header is malformed (missing the `Bearer ` prefix).

**Resolution steps:**
1. Confirm the header is formatted as `Authorization: Bearer <token>`.
2. Check token age — tokens older than 60 minutes must be refreshed using the `/oauth/token` endpoint with `grant_type=refresh_token`.
3. If the refresh token itself returns `invalid_grant`, the refresh token has likely expired (refresh tokens expire after 30 days of inactivity) and the user must re-authenticate via OAuth flow.

### 2.2 Error: `403 FORBIDDEN` — `insufficient_scope`
The token is valid but lacks the required OAuth scope for the endpoint being called (e.g., calling `/contacts/write` with a token that only has `contacts:read` scope).

**Resolution:** Re-authorize the integration requesting the additional scope, or check the app's configured scopes in **Settings → Developer → OAuth Apps**.

## 3. Rate Limiting

Nimbus enforces the following default rate limits per API key:

| Plan | Requests/minute | Burst allowance |
|------|------------------|-----------------|
| Starter | 60 | 10 |
| Growth | 300 | 50 |
| Enterprise | 1,200 | 200 |

When a limit is exceeded, the API returns `HTTP 429 Too Many Requests` with a `Retry-After` header (in seconds) and an `X-RateLimit-Remaining: 0` header.

**Best practice:** Implement exponential backoff. Do not retry immediately on a 429 — repeated immediate retries can trigger a temporary IP-level throttle (separate from the key-level limit) lasting up to 15 minutes.

## 4. Common Error Codes

| HTTP Status | Error Code | Meaning | Typical Cause |
|---|---|---|---|
| 400 | `validation_error` | Request body failed schema validation | Missing required field, wrong data type |
| 401 | `invalid_token` | Token missing, expired, or malformed | See Section 2.1 |
| 403 | `insufficient_scope` | Token lacks required permission | See Section 2.2 |
| 404 | `resource_not_found` | Object ID does not exist or was deleted | Stale cached ID, wrong environment (sandbox vs. live) |
| 409 | `duplicate_resource` | Unique constraint violation (e.g., duplicate email on a contact) | Idempotency key reused with different payload |
| 422 | `unprocessable_entity` | Request is well-formed but semantically invalid | E.g., setting an end date before a start date |
| 429 | `rate_limit_exceeded` | Too many requests in the rate window | See Section 3 |
| 500 | `internal_error` | Unhandled server-side exception | Transient — retry with backoff; escalate if persistent |
| 503 | `service_unavailable` | Platform in maintenance or degraded mode | Check status.nimbuscloud.io |

## 5. Idempotency

All `POST` endpoints accept an optional `Idempotency-Key` header (any unique string, max 255 chars). If the same key is sent twice with an **identical** payload, Nimbus returns the original cached response instead of creating a duplicate record. If the same key is sent with a **different** payload, the API returns `409 duplicate_resource` to prevent silent data corruption.

Idempotency keys are stored for 24 hours. After that window, reusing a key is treated as a brand-new request.

## 6. Webhooks Not Firing

If configured webhooks are not being delivered:
1. Check **Settings → Developer → Webhooks → Delivery Log** for failed attempts and response codes.
2. Nimbus retries failed webhook deliveries 5 times with exponential backoff (1m, 5m, 15m, 1h, 6h). After 5 failures, the webhook subscription is automatically marked `disabled` and must be manually re-enabled.
3. Verify your endpoint returns a `2xx` status within 10 seconds — slower responses are treated as failures even if processing eventually succeeds.
4. Confirm the payload signature using the `X-Nimbus-Signature` HMAC-SHA256 header to rule out a rejected request on your end due to signature mismatch.

## 7. CORS Errors in Browser-Based Integrations

Direct calls to `api.nimbuscloud.io` from client-side JavaScript will fail with a CORS error — the API does not allow browser-origin requests for security reasons (API keys must never be exposed client-side). All browser-based integrations must proxy requests through a backend server. This is by design, not a bug.

## 8. Sandbox vs. Production Environments

Sandbox base URL: `sandbox-api.nimbuscloud.io/v2`
Production base URL: `api.nimbuscloud.io/v2`

A common support ticket is "my records aren't showing up" — in most cases this is because the integration was tested against sandbox but the user is checking the production dashboard (or vice versa). Sandbox data is purged every 30 days and is never synced to production.

## 9. When to Escalate to Engineering

Escalate (do not attempt further self-service troubleshooting) if:
- `500` or `503` errors persist for more than 10 minutes across multiple endpoints.
- Webhook delivery logs show signature verification failing despite confirmed correct shared secret.
- A customer reports data corruption (e.g., fields silently overwritten) rather than a request failure.
