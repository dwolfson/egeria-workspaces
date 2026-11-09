# Portal caches

The Portal keeps several short-lived, in-memory caches so that tree views, lists and dashboards open quickly. This page says whose data a cache entry belongs to, and what happens when a sign-in expires. It describes behaviour; the code is in `result_cache.py` and the handlers that use it.

## Whose entry is it?

Egeria shows different people different elements (governance zones), so a cached answer must only ever go back to the person it was fetched for. The Portal therefore keys each entry on **the credential that was presented with the request**, not on a name the request claims:

- A request with a token (`X-Egeria-Token`) is keyed on a hash of the whole token.
- A request with a user id and password is keyed on a hash of both.
- A request with neither is keyed as the Portal's own service user.

This is `result_cache.credential_identity`; handlers get it for the current request from `result_cache.request_identity(user_id, user_pwd)`. Only a hash is kept, in memory, and never logged. A token's own claims (such as its `sub`) and a bare user id are not used, because anyone can write them: someone who forged one could otherwise read another person's cached data. A forged credential produces a key nobody else has, so it misses the cache, goes to Egeria, and is refused. A refusal is never cached.

A renewed token is a new key, so the first request after renewing is a miss.

## An expired token is never served from cache

If the token on a request has expired, `request_identity` returns nothing, and the handler neither reads nor fills its cache. The request goes to Egeria and is refused, so the person is asked to sign in again instead of carrying on with data cached under their old sign-in. Caches that are built in the background refuse in the same way, rather than start a long Egeria call that would only be refused.

These caches use the presented credential: collection, digital product and project trees, solution-architect folios and component trees, governance metrics, integration connector reports, engine actions, the oldest-created-element lookup, the Overview totals, activity and people panels, Local Dashboards report look-ups, and the Catalog and Resource Browser lists. The Type Explorer's type definitions are the same for everyone and are shared.

Every key also carries the **as-of time** where a view has one, and the **Promise / Memento toggle** setting, so the same screen at a different time or toggle setting is a different entry.

## Dashboard results

Local Dashboards run each Report placement through `/api/report-specs/execute` with caching on. Each result is stored under the report spec, format, parameters, platform, the viewer's credential, persona and the Promise / Memento toggle.

| State | When | What the viewer gets |
|---|---|---|
| fresh | stored less than 5 minutes ago (`PORTAL_RESULT_CACHE_TTL`) | the stored result, nothing is run |
| stale | older than that, up to an hour | the stored result now, and one background refresh |
| miss | absent or older than an hour | the report runs, and the viewer waits |

Only one run per key is in flight at a time; other requests for it wait for that run. A viewer's refresh skips the stored result and runs now. The store holds at most 256 results (`PORTAL_RESULT_CACHE_MAX`), dropping the least recently used, and results larger than about 2 MB are served but not stored. Errors, refusals and token failures are never stored. The Report Specs browser's own **Run** never uses the cache.
