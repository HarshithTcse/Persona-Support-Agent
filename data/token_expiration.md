# Token Expiration & Session Management

**Product:** Nimbus Cloud Platform
**Category:** Authentication
**Last updated:** February 2026

## 1. Token Types

Nimbus uses three distinct token types, each with different lifetimes and purposes:

| Token Type | Lifetime | Purpose | Where Used |
|---|---|---|---|
| Access Token | 60 minutes | Authorizes individual API requests | `Authorization: Bearer` header |
| Refresh Token | 30 days (sliding — renewed on each use) | Obtains a new access token without re-login | Server-side OAuth flows only |
| Session Cookie | 14 days (sliding) or until logout | Keeps a user logged into the web dashboard | Browser session |

## 2. Access Token Expiration

Access tokens are intentionally short-lived (60 minutes) to limit the impact of a leaked token. When an access token expires, API calls return:

```json
{
  "error": "invalid_token",
  "error_description": "The access token expired",
  "status": 401
}
```

**Fix:** Call `POST /oauth/token` with `grant_type=refresh_token` and the stored refresh token to obtain a new access token. Well-built integrations should refresh proactively a few minutes before the 60-minute mark rather than waiting for a 401.

## 3. Refresh Token Expiration

Refresh tokens expire after **30 days of non-use** (each successful refresh resets the 30-day clock). If a refresh token has expired:

```json
{
  "error": "invalid_grant",
  "error_description": "Refresh token expired or revoked",
  "status": 400
}
```

There is no way to recover an expired refresh token — the integration must complete the full OAuth authorization flow again, which requires the end user to log in and approve access. This commonly happens with integrations that run on an infrequent schedule (e.g., a monthly batch job) where the 30-day window lapses between runs.

**Recommendation for developers:** If your integration runs less than once every 30 days, implement a "keep-alive" refresh call on a recurring schedule (e.g., weekly) purely to prevent the refresh token from expiring.

## 4. Refresh Token Revocation

Refresh tokens are immediately revoked (regardless of remaining lifetime) when:
- The user manually disconnects the integration from **Settings → Developer → OAuth Apps → Connected Apps**.
- The user changes their password.
- An admin removes the user's seat from the workspace.
- A security hold is triggered on the account (see `account_lockout.md`).

## 5. Session Cookie Expiration (Dashboard)

Dashboard sessions use a sliding 14-day expiration — every page load resets the countdown, so an actively used session effectively never expires, while an idle session logs out automatically after 14 days of inactivity. Closing the browser does not end the session unless "Remember this device" was left unchecked at login.

## 6. JWT-Based Single Sign-On (SSO) Tokens

For Enterprise customers using SAML or OIDC SSO, the Identity Provider (IdP) issues a SAML assertion or OIDC ID token with its own expiration, set entirely by the customer's IdP configuration (not controlled by Nimbus). If users on SSO are logged out more frequently than expected, this is almost always an IdP-side session timeout setting, not a Nimbus token issue — escalate to the customer's IT admin to check their IdP session policy.

## 7. Troubleshooting Checklist

When a user reports unexpected logouts or repeated `401` errors:
1. Confirm whether they are using SSO — if so, this is likely an IdP configuration issue (Section 6).
2. Check whether their integration refreshes tokens proactively or only reactively on 401 (Section 2).
3. Check the OAuth Apps connection log for revocation events (Section 4) — a password change or admin seat removal will silently break existing integrations until reconnected.
4. For dashboard-only users (not API), confirm "Remember this device" was checked, and check for browser extensions that clear cookies automatically.

## 8. Security Note

Nimbus never sends access or refresh tokens via email or support chat for any reason, even to verified account owners. If a customer requests this, it must be declined and the request should be treated as a potential social-engineering attempt requiring escalation.
