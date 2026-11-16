<!-- DRAFT: new file docs/release-notes/6.2.x-egeria-6.3.md in odpi/egeria-python.
     An aggregate overview; the per-version files (6.2.26.md onwards) are not changed.
     Range v6.2.0 (c9dc7a43, 2026-10-08) to v6.2.39 (18178917, 2026-11-12). 6.2.38 was tagged but not published to PyPI;
     6.2.39 carries its fixes. Numbers are PRs in odpi/egeria-python. -->

<!-- pyegeria 6.3.0 is planned with the cut (Coordinator, 2026-11-16): its section is drafted in pyegeria-6.3.0-section-DRAFT.md. -->
<!-- TODO at the cut: extend to 6.2.40/6.2.41/6.2.42 (#593, #595, #598; owner 2026-11-16: 6.2.42 is the floor the release notes state everywhere). -->

# pyegeria 6.2.0 → 6.2.39 (Egeria 6.3)

We released pyegeria 39 times between 6.2.0 (October 8, 2026) and 6.2.39 (November 12, 2026), about four releases a
week. (6.2.38 was tagged but not published to PyPI; 6.2.39 includes its fixes.) Together they make up the Python side
of **Egeria 6.3**. This page groups the releases by theme, so you can see what changed without reading each one. The per-release notes from 6.2.26 onwards are in this folder; earlier releases are
described in their release PRs.

**If you are upgrading from 6.2.0, read [Behaviour changes](#behaviour-changes) first.**

```bash
pip install -U pyegeria
```

## Report specs and analytic functions

- **Found by registered name.** Analytic functions resolve by registry name or an allowed module prefix (#516), can
  carry a declaration (#517), say why a result is absent instead of returning it as data (#518), and are discovered
  from installed packages (#519). Report specs are found by registered name, with `pyegeria.report_specs` entry points
  (6.2.18, #523).
- **Every routine declares itself** (6.2.24, #539) and a routine's declaration and bindings are first-class, with
  `AnalyticFunctionSpec` as a view of them (#546).
- **Every report spec is resolved when it loads**; specs that cannot run are listed with the reason
  (6.2.25, #548). The executor supplies declared inputs by role (6.2.26, #552), and the old analytic binder is removed
  (#553). See [Routines, declarations and roles](../output-formats-and-report-specs.md#routines-declarations-and-roles).
- **Report specs held in Egeria**, run from plain pyegeria (6.2.28, #563, #564, #569); specs are organised in consumer
  folders with a recursive sync and consumer index (6.2.33, #582); restricted specs (6.2.35, #587).
- **Search and get filters** are universal, checked and typed (6.2.28, #567).
- **Standard documents and complex values** (6.2.37, #589): a DOCUMENT output type with validators that never fetch
  over the network, and a built-in **DCAT Catalog** spec that exports a collection's Assets as a DCAT-AP 3 catalog,
  validated against the shipped SHACL shapes; an opt-in structured TABLE (`table_shape="structured"`) and native DICT
  (`dict_shape="native"`), with per-column render intents. Existing calls return the same shapes. The DCAT Catalog
  runs with a search string as well as a scope (6.2.38, #590). See
  [Output formats and report specs](../output-formats-and-report-specs.md) (#592).

## Dashboards and measurements (Egeria 6.3)

- **Client and Dr.Egeria commands** for Egeria 6.3 report specs, measurements and dashboards (6.2.24, #540, #541).
- **Dashboard sheets** are written as Egeria 6.3 Dashboard elements (#570), read from Egeria (#571), held with an
  owner (6.2.31, #578), and organised in Egeria folders, with a sheet's spec fetched as the viewer (#586).
- **Collection Members by qualifiedName**, `saved_query` reports, exact trend points and the Saved Query Formula
  (6.2.34, #585); Saved Query delete, Smart Collections by catalog target, and report parameters on dashboard Reports
  (6.2.35, #587).

## Overview metrics: measured or not measured

- **A value that wasn't measured is `None`, not 0** (6.2.22, #531; opt-in strict counts since #448). A count that hit
  its cap or timed out is reported as not measured, rather than as the cap (#555); scans either read every page or
  report nothing (#565).
- **`asset_composition`**, with a subtype tree and two count scopes (6.2.23, #534); the absence word `nothing_found`
  (#535).
- **`population=`** is the count keyword; `scope=` is deprecated (6.2.24, #538).
- **Totals count the whole repository** by default (6.2.27, #556); `stale_assets` counted by update-time bisection (#572).

## Dr.Egeria

- **Reference Data** authoring, and the Valid Metadata family split (6.2.3, #449).
- **Credentials resolved at run time** with one precedence chain (#477); Postgres commands take a secrets store (#478).
- **Updates no longer reset properties the document doesn't set** (6.2.10, #482).
- **New commands**: Business Capability, Business Capability Dependency and Digital Support (6.2.11, #486); statements
  of applicability (#492, #493); survey reports and security findings (#497).
- **Link and detach commands that reported success but sent nothing** are fixed (6.2.28, #566).
- **Zone Membership in Basic templates**; blank zones are no longer cleared (6.2.30, #577).
- **Parent ID keeps memberships**, templates ship as package data, and a dashboard resolver (6.2.32, #581).
- **A bullet in a list attribute is one item**, commas and all (6.2.39, #591). Write list values as bullets.

## Egeria 6.3 compatibility

- Governance Engine client for the engine-action operations Egeria moved (6.2.5, #460).
- Boxed properties, and a failed bearer-token request now raises (6.2.13, #498).
- Information supply chain mermaid graphs (6.2.14, #503); every Egeria graph key, with action and activity graphs
  beside the context graph (6.2.29, #573).
- Lineage graph `maxHops` and `skipRelationships` (#526).
- Configurable TLS verification of the platform certificate (#530).
- Endpoints Egeria removed are routed to their replacements and deprecated (#485); `get_platform_organization` reads
  `/api/public/app/info` (6.2.11, #487).
- `NotificationType` drops `notificationInterval`; subscription types use `minimumNotificationInterval` (#558).
- Security annotation models and findings/posture reports (#495).

## My Egeria (formerly My Profile)

- One key-binding convention and a discoverable My Team view (#463, #469); My Network option (#458).
- Renamed to `my_egeria.py` (6.2.12, #491); login as a different user and no-Egeria startup handling (#501, #507).
- Edit Profile saves to Egeria (#524).
- Promoted to a production package (#580), with a recorded video blog and voiceover pipeline (#584).
- Selecting a business domain passes the GUID (6.2.38, #590).

## Correctness

- Five update methods that sent no body (6.2.7, #471).
- Request fields silently dropped SDK-wide (6.2.10, #483).
- By-name wrappers: the type filter reaches Egeria, and a body-only call is accepted (#439, #445).
- Template builders gained the placeholders Egeria added (#474, #475).
- Link methods return relationship GUIDs; Pydantic V2 (6.2.19, #525). Five link methods named a properties class
  Egeria lacks (#537).
- A caller-supplied token is not re-authenticated as the client's user (6.2.15, #508).
- **Runs without `nest_asyncio`, so pyegeria works on Python 3.14** (6.2.16, #513).
- `get_collection_members` pages; folder walks page every folder; no paging loop can run forever (6.2.36, #588,
  ISSUE-185).

## Security

- certifi floor excluding the distrusted emSign G3 root, and tornado 6.6 (6.2.21, #529).

## Behaviour changes

| Since | Change | What to do |
|---|---|---|
| 6.2.13 | A failed bearer-token request raises instead of returning quietly (#498). | Catch the exception where you handled an empty token. |
| 6.2.19 | Link methods return the relationship GUID (#525). | Use the return value if you need the relationship. |
| 6.2.22 | Unmeasured overview counts are `None`, not 0 (#531). | Treat `None` as "not measured"; don't add it as 0. |
| 6.2.23 | Absence word `nothing_found`; the legacy `measured_nothing` is still read (#535). | Write `nothing_found`. |
| 6.2.24 | `population=` replaces `scope=` on overview counts; `scope=` is deprecated (#538). | Rename the keyword. |
| 6.2.26 | The analytic binder is removed; inputs are supplied by role (#552, #553). A spec that still carries `analytic_binders` warns (#561). | Declare `inputs` on the routine. |
| 6.2.27 | Totals count the whole repository by default (#556). | Expect larger, correct totals. |
| 6.2.34 | An element hidden by zone security is reported as `AUTHORIZATION_ERROR_403`, not `_401`; the exception class is unchanged and a 403 is never retried (#585, ISSUE-182). | If you match `AUTHORIZATION_ERROR_401` in the text, match `AUTHORIZATION_ERROR` instead. |
| 6.2.36 | With `body=` and no paging in the body, the method's `page_size` default now applies on 19 methods (#588). | Put `pageSize` in the body, or pass `page_size`, if you relied on Egeria's default page. See [6.2.36](6.2.36.md). |
| 6.2.37 | Rendered **text** changes (REPORT, LIST, MD, FORM, HTML, the CLI table): LIST cells are drawn by what the value is, and capped results say "more may exist" (#589). Result shapes are unchanged. | Re-check anything that parses pyegeria's rendered text; read DICT or JSON instead. See [6.2.37](6.2.37.md). |
| 6.2.39 | Dr.Egeria: a single bullet on its own line, such as "- a, b", is one item (it used to be two) (#591). | Write one item per bullet. See [6.2.39](6.2.39.md). |

## Dependencies and housekeeping

- multidict 6.9.1 (#437); codeql-action and action-gh-release bumps (#441, #442, #559, #560); consolidated Dependabot
  updates (#502).
- The issue trackers (`PYEGERIA_ISSUES.md`, `EGERIA_OPEN_ISSUES.md`) were re-derived and kept current through the
  Egeria re-test passes.

## Release-by-release

| Version | Date | Release PR |
|---|---|---|
| 6.2.1 – 6.2.10 | Oct 10 – Oct 23 | #443, #447, #455, #459, #461, #467, #473, #476, #479, #484 |
| 6.2.11 – 6.2.20 | Oct 24 – Nov 3 | #487, #494, #499, #504, #511, #515, #522, #523, #525, #527 |
| 6.2.21 – 6.2.30 | Nov 4 – Nov 10 | #529, #533, #536, #545, #551, #554, #557, #568, #575, #577 |
| 6.2.31 – 6.2.39 | Nov 10 – Nov 12 | #578, #581, #583, #585, #587, #588, #589, #590, #591 |

Detailed notes: [6.2.26](6.2.26.md) · [6.2.27](6.2.27.md) · [6.2.28](6.2.28.md) · [6.2.29](6.2.29.md) ·
[6.2.30](6.2.30.md) · [6.2.31](6.2.31.md) · [6.2.32](6.2.32.md) · [6.2.33](6.2.33.md) · [6.2.34](6.2.34.md) ·
[6.2.35](6.2.35.md) · [6.2.36](6.2.36.md) · [6.2.37](6.2.37.md) · [6.2.38](6.2.38.md) · [6.2.39](6.2.39.md)
