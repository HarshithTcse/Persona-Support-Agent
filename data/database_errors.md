# Database Errors & Data Issues

**Product:** Nimbus Cloud Platform
**Category:** Platform Reliability / Data Integrity
**Last updated:** March 2026

## 1. Overview

This guide covers database-layer errors that surface to customers, primarily through the API (as `5xx` responses) or as data inconsistencies in the dashboard. It is intended to help support agents distinguish transient, self-resolving issues from those requiring engineering escalation.

## 2. Common Error Codes

| Code | Name | Meaning | Customer-Facing Symptom |
|---|---|---|---|
| `DB_CONN_TIMEOUT` | Connection Timeout | The application server could not establish a connection to the database within 5 seconds | API request hangs, then returns `503` |
| `DB_POOL_EXHAUSTED` | Connection Pool Exhausted | All available database connections are in use; new requests must wait or fail | Intermittent `503` errors during high-traffic periods |
| `DB_QUERY_TIMEOUT` | Query Timeout | A query ran longer than the 30-second execution limit and was killed | Specific report or export operation fails with `504` |
| `DB_REPLICA_LAG` | Replication Lag | The read replica serving a request is behind the primary database by more than 5 seconds | Recently created/updated records temporarily don't appear in reads |
| `DB_CONSTRAINT_VIOLATION` | Constraint Violation | An operation would violate a uniqueness or foreign-key constraint | `409` error on the API; usually a legitimate data conflict, not a bug |
| `DB_DEADLOCK` | Deadlock Detected | Two concurrent transactions were waiting on each other; one was automatically rolled back | Operation fails and should be safely retried |

## 3. Connection Pool Exhaustion (`DB_POOL_EXHAUSTED`)

This is the most common cause of intermittent `503` errors during traffic spikes (e.g., a large customer running a bulk import while normal traffic continues). It is:
- **Self-resolving** within 1–2 minutes as load decreases and connections free up.
- **Not** indicative of data loss — requests that fail with this error were never committed, so there is no partial/corrupted write to worry about.

If reported by multiple customers simultaneously, check the internal infrastructure dashboard (not customer-facing) for current pool utilization before responding — this may indicate a genuine capacity issue requiring infrastructure scaling rather than a one-off spike.

## 4. Replication Lag (`DB_REPLICA_LAG`)

Nimbus uses a primary-replica database architecture: writes go to the primary; most reads (dashboard views, reports, API `GET` requests) are served from read replicas for performance. Under normal conditions, replication lag is under 200ms and invisible to users. During lag spikes (rare, typically under 5 minutes), customers may report "I just created a contact but it's not showing up in my list" — this is expected, temporary, eventually-consistent behavior, not data loss. Refreshing after a minute resolves it.

**Note:** Critical operations like billing and authentication always read from the primary database directly, never replicas, specifically to avoid consistency issues in security-sensitive flows.

## 5. Query Timeouts on Large Exports/Reports

Reports or data exports involving very large datasets (typically >200,000 records with complex filtering) can exceed the 30-second query timeout. This is by design to protect overall database performance from a single expensive query monopolizing resources.

**Workaround:** Recommend the customer narrow the date range or filter criteria to reduce the result set, or use the **Async Export** feature (Settings → Data → Export → "Run as background job"), which has no timeout and emails a download link when complete, typically within 10–30 minutes for very large datasets.

## 6. Constraint Violations Reported as "Bugs"

Customers occasionally report `409 DB_CONSTRAINT_VIOLATION` errors as bugs when they are in fact correct behavior — e.g., attempting to import a CSV with duplicate email addresses when "Email" is configured as the unique matching key for contacts. Before escalating, confirm:
1. What unique constraint was violated (visible in the error detail field).
2. Whether the customer's data genuinely contains duplicates against that field.

## 7. When to Escalate to Engineering

Escalate immediately, rather than offering further self-service troubleshooting, when:
- Errors persist beyond the expected self-resolving windows described above (pool exhaustion >5 minutes, replication lag >10 minutes).
- A customer reports data that was present and is now missing entirely (not just delayed) — this is treated as a potential data-integrity incident, not a performance issue, and follows the incident process in `service_outage.md`.
- Deadlocks (`DB_DEADLOCK`) are reported repeatedly on the same operation type, which may indicate an application-level locking bug rather than normal concurrent-access contention.
- Any database error is accompanied by a report of incorrect data appearing on a *different* customer's account — this is escalated as a critical, highest-priority data isolation concern regardless of how minor it seems.
