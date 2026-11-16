# Running release notes for the next release

**Status.** Living draft, revised 2026-11-11. The Coordinator keeps adding to it until the release (planned in a few days). It covers everything merged since the previous published notes, the October 2026 newsletter (https://egeria-project.org/release-notes/october-2026/, added to egeria-docs on 2026-10-09 in commit fb489c6b). That newsletter announced Egeria 6.1/6.2, said Workspaces was updated alongside 6.2, and described Resource Explorer and Egeria Advisor as "early previews". The first half follows the newsletter's shape (What's new, then one section per product). The second half is a detailed appendix with PR numbers. Entries come from merge-commit and PR titles. Where a PR's effect was not clear from its title the bullet says "(see PR)". Nothing has been verified on a running system.

## Baselines

All three baselines are the state of each repo on **2026-10-09**, the date the October newsletter was published.

| Repo | Baseline | Date | Head | How chosen |
|---|---|---|---|---|
| egeria-workspaces (`odpi/egeria-workspaces`) | `903e8eeb`, merge of #619 "prepare 6.2" | 2026-10-09 | `3b8ac7e2` (2026-11-12, #857) | The 6.2 release-prep merge, tagged `v6.2` on 2026-11-11. 217 first-parent entries since. |
| pyegeria (`odpi/egeria-python`) | tag `v6.2.0` = `c9dc7a43` | 2026-10-08 | `d757cb2c` (2026-11-12, #592; `v6.2.39` = `18178917`) | Newest tag not after 2026-10-09. The next tag, `v6.2.1`, is dated 2026-10-10. 39 releases (6.2.1 to 6.2.39; 6.2.38 tagged but not on PyPI). `upstream/main` is one docs PR beyond 6.2.39. |
| trellis (`dwolfson/trellis`) | `b74b07f9` "RE: baseline the best-effort client close in the data-class rules lookup" | 2026-10-09 17:31 -0500 | `73738df8` (2026-11-12, #1086) | Last commit at or before 2026-10-09 23:59 UTC (`git rev-list -1 --before=...`). The repo has no tags or CHANGELOG. About 523 distinct PR numbers and 1,151 non-merge commits since. |

Notes:
- trellis PRs are `dwolfson/trellis#N`. About 20 odpi-side Dependabot bumps (#80 to #107) reached it through the sync merge #112 and are not itemised.
- In egeria-workspaces, #829 (LD-2 dashboard folder seeds) and #830 (LD-3 Portal Local Dashboards by folder) are **already merged** (2026-11-11), not pending.
- The October newsletter was re-read on 2026-11-11 from egeria-docs `origin/main` (`site/docs/release-notes/october-2026.md`); the local egeria-docs checkout is behind and does not have it.

## Merge-check log

| When (UTC) | workspaces upstream | pyegeria upstream | trellis origin | Folded in |
|---|---|---|---|---|
| 2026-11-11 | `48c94577` (#830), nothing new | `e2f048d8` (v6.2.36), nothing new | `c9892ec2` | trellis #1076 (pyegeria floor 6.2.36 for RE and EA), #1077 (EA: Egeria 5xx at Portal SSO is "unreachable", not "rejected"), #1078 (EA feedback: a changed vote supersedes the earlier one; the recorded intent is the routed intent) |
| 2026-11-12 | `3b8ac7e2` (#857): #831–#857 (22 first-parent entries, 8 of them Dependabot) | `d757cb2c`: 6.2.37 (#589), 6.2.38 (#590, not on PyPI), 6.2.39 (#591), docs #592 | `73738df8` (#1086): #1079–#1086 | All of them, in every variation: workspaces 6.3 section (new Nov 8–12 bullets, upgrade notes, stats 377/217), CHANGELOG cut (Added/Fixed), trellis CHANGELOG and notes (floor 6.2.39, EA tables/folders/count tile), pyegeria overview (6.2.37–6.2.39 themes, behaviour changes, release table), overview and newsletter numbers |

---

# What's new

## Dashboards and report specs now live in Egeria

The biggest change since October. Local Dashboards used to be files; the dashboard sheets, their tiles and the report specs that feed them can now be held in Egeria itself, organised in folders, and the Portal reads them from there. Report specs are filed by the tool that uses them (Portal, Egeria Advisor, Resource Explorer, pyegeria, My Egeria, Jupyter), and the Egeria Explorer shows a "Used by" row for each spec. The Portal shows each spec's declarations, whether it can be run, and, when it can't, why. Four new "useful" dashboard sheets and repository trend tiles are seeded in the demo. pyegeria 6.2.28 to 6.2.35 carry the matching client, Dr.Egeria commands and resolver.
Learn more: `portal-docs/tools/local-dashboards.md`, `portal-docs/tutorials/local-dashboards.md`, `portal-docs/tutorials/report-specs.md`, `portal-docs/Internals/report-specs-dashboards-egeria-model.md`.

## Numbers that say what they measured

The Overview page and report results no longer turn "not measured" into 0 or a cap into a total. Whole-repository counts, background measurement of slow sections, explicit count populations and "not measured" cards replace the old behaviour. pyegeria 6.2.22 onwards returns `None` for an unmeasured count; Resource Explorer applies the same rule (for example an unsurveyed database is "not established").
Learn more: `portal-docs/tools/egeria-overview.md`.

## Relationships grouped by purpose; every width is yours to change

Egeria gives every relationship type a purpose. The Portal groups relationships into six families (Composition, Governance & Description, Organization, Associations, Design & Deployment, Operations) in the Type Explorer, detail panels, Data Mesh and The Catalog. Every column, pane and split in the Portal can now be dragged and the width is remembered per page.
Learn more: `portal-docs/tools/egeria-explorer.md` ("Relationship purposes", "Resizing").

## Tutorials and analytic functions

New tutorials cover saved queries, writing and registering analytic functions, report specs and local dashboards, each with worked examples. Analytic functions and report specs are now found by registered name (pyegeria 6.2.16 to 6.2.18).
Learn more: `portal-docs/tutorials/overview.md`.

## Demo stack and security

The demo now isolates its workbenches behind an egress allow-list, binds published ports to 127.0.0.1 by default (`--lan` opens them), starts Airflow and Marquez with lineage flowing to Egeria, and has self-healing containers. After the Obsidian compromise the public demo was hardened. The Portal only sends credentials to allow-listed platforms, a signed-in user's request is never run as the service account, and Jupyter and the images no longer trust the distrusted emSign ECC G3 root.

---

# Egeria Workspaces

Everything is in the Portal and the quickstart/freshstart stacks. CHANGELOG.md `[Unreleased]` has fuller text.

- **Resource Browser and Resource Locator.** A new Resource Browser: a resource page with what it contains, its meaning and notes on its parts; search, home and browse; work lists and team sharing. Learn more: `portal-docs/tools/resource-locator.md`.
- **Curation Coverage tile.** Resource Explorer's curation coverage appears as a Dashboard Sheet tile.
- **Egeria Explorer.** Inheritance for relationship and classification types; a Classifications tab; "Used by" chips and consumer filter on report specs. Learn more: `portal-docs/tools/egeria-explorer.md`.
- **The Catalog.** Infrastructure subtype tabs, View buttons on schema rows, every list pages to the end (large ones capped visibly), Data Assets show every type as a tree. Learn more: `portal-docs/tools/tech-catalog.md`.
- **Data initialization can run notebooks** and scans roots for manifests. Learn more: `portal-docs/tools/data-initialization-notebooks.md`.
- **Lineage Explorer** gets a hop limit, cut markers and relationship scope (Egeria 6.3).
- **Coco Pharmaceuticals demo content.** A Chief Data Officer dashboard for Jules Keeper, security support, sustainability reference data, Airflow DAGs that animate the digital products.
- **Platform.** Quickstart and freshstart moved to Egeria 6.3-SNAPSHOT; the quickstart pin tracks the Pasteur build. Freshstart is capped below pyegeria 6.2.27.
- **Egeria Advisor** gets its own service account (`egeriaadvisornpa`) in quickstart (odpi/egeria-workspaces#828).

# Resource Explorer and Egeria Advisor (trellis)

In the October newsletter these were "early previews". Since then they have been worked on daily (about 500 merged PRs) and both are now much closer to a product. Learn more: `docs/trellis-architecture.md`, `docs/trellis-journey.md`, and in the Portal `portal-docs/tools/resource-explorer.md` and `portal-docs/tools/egeria-advisor.md`.

**Resource Explorer**
- **Publishes to Egeria.** Curated results are published as Egeria elements with read-back, correct zoning (zone what it produced, never what it references; private members publish only as their owner), and a Publish button with plain-language failures.
- **Surveys run through Egeria.** Resource Explorer's surveys are registered as Survey Definitions that Egeria's engine host can run (one card per definition, with run line, history and Cancel). Every step emits an OpenLineage run event.
- **Deeper database analysis.** Table flags, materialized views, database activity, per-table sizes, value profiles and quality checks that publish as Egeria quality annotations (a 5-minute per-table budget).
- **Files and open data.** File systems are surveyed (Egeria's CSV survey, Parquet profile, Delta Lake layout signal, narrative passages searched by chat); open-data repositories (DOI, DataCite, DCAT-AP) can be published as a dataset with a read-back.
- **A better chat.** Questions about a resource search that resource's docs first, cross-asset links carry a stated confidence band, link totals lead the answer, answers render markdown, and the first index of a repository is asked about first.
- **A new UI.** The Next UI has a Look control (Dark, Light, Paper), cards and tiles, a graph renderer, resizable tables, and in-page prompts instead of browser dialogs.
- **Closed-loop feedback and re-index.** Ratings carry a cause and evidence, an admin triages them, a diagnosis can be routed to a gap; the document index can be rebuilt, swapped and rolled back.
- **Safer by default.** Caller identity is adopted on every route, a dead token is answered the same way everywhere, the plaintext DB credential fallback is gone, non-JWT tokens are refused at login, and a zone with no access control is private (matches Egeria).
- **Tutorial.** Parts 1 to 6 are written (what Resource Explorer is for, sign in, add data sources and more).

**Egeria Advisor**
- Reads and authors Dashboards in Egeria (parity with the Portal), publishes report specs (restricted publish stays off until proven), maps perspectives to role profiles.
- Security hardening: Dr.Egeria runs as the signed-in user, calls with neither token nor password are refused, an Admin link shown only to admins, no sessions for service accounts, sanitised rendering.
- Uses the shared feedback library and the shared `trellis-ui` looks.

**Shared packages.** New `trellis-feedback` (0.1 to 0.3), `trellis-ui`, and a `trellis-accel` package for choosing a compute device (work in progress). The Analytic Library moved out as `egeria-trellis-analytics` 0.2.0 on PyPI.
Learn more: `docs/feedback-closed-loop-design.md`, `docs/hardware-acceleration-proposal.md`, `docs/context-compilation-usage.md`.

# pyegeria (6.2.0 to 6.2.39)

39 releases in five weeks (about 4 a week). Grouped by theme, with the first version where a notable item landed.

- **Report specs and analytic functions.** Found by registered name and the `pyegeria.report_specs` entry points (6.2.16 to 6.2.18); every routine has a declaration (6.2.24); every spec resolved at load, unrunnable ones listed with reasons (6.2.25); specs held in Egeria and run from plain pyegeria (6.2.28); consumer folders (6.2.33); restricted specs (6.2.35); DOCUMENT output with validators and the DCAT Catalog spec, structured TABLE and native DICT, per-column render intents (6.2.37); DCAT Catalog by search string (6.2.38).
- **Dashboards and measurements (Egeria 6.3).** Client and Dr.Egeria commands for report specs, measurements and dashboards (6.2.24); Dashboard Sheets read from and held in Egeria with an owner (6.2.28, 6.2.31); sheets in Egeria folders (by 6.2.34); Collection Members by qualifiedName and `saved_query` reports (6.2.34); report parameters on dashboard Reports (6.2.35).
- **Overview metrics that say what they measured.** `None` instead of 0 when unmeasured (6.2.22); `asset_composition` routine (6.2.23); whole-repository counts by default (6.2.27); `population=` replaces `scope=` (6.2.24); stale-asset counting fixed (6.2.29).
- **Dr.Egeria.** Reference Data authoring and Valid Metadata split (6.2.3); credentials resolved at run time with one precedence chain, Postgres secrets store (6.2.9); updates no longer reset properties the document doesn't set (6.2.10); Business Capability commands (6.2.11); Security Officer statements of applicability, survey report and security finding commands (6.2.12, 6.2.13); link/detach commands that reported success but sent nothing fixed (6.2.28); Zone Membership in Basic templates (6.2.30); Parent ID keeps memberships, templates ship as package data (6.2.32); a bullet in a list attribute is one item, commas and all (6.2.39).
- **Egeria 6.3 compatibility.** Boxed properties and a raising bearer-token request (6.2.13); information supply chain graphs (6.2.14); lineage `maxHops`/`skipRelationships` (6.2.20); configurable TLS verification (6.2.22); all graph keys (6.2.29).
- **My Egeria / My Profile.** One key-binding convention and discoverable My Team (6.2.4 to 6.2.7); rename to `my_egeria.py` (6.2.12); Edit Profile saves to Egeria (6.2.19); promoted to a production package (6.2.33 timeframe).
- **Correctness.** Five update methods that sent no body (6.2.7); request fields silently dropped SDK-wide (6.2.10); link methods return relationship GUIDs (6.2.19); caller-supplied tokens are not re-authenticated (6.2.15); runs without `nest_asyncio` so it works on Python 3.14 (6.2.16); collection members and folder walks page properly (6.2.36, ISSUE-185).
- **Security.** certifi floor excluding the distrusted emSign G3 root and tornado 6.6 (6.2.21).

### Unreleased since v6.2.39
- Docs only: report specs after 6.2.37 (complex values, render intents, DOCUMENT, surfaces) (#592).

### Released since the first draft (2026-11-12 merge check)
- **6.2.37** (#589): SD-1 DOCUMENT output and validators, SD-2 DCAT Catalog export, structured TABLE, native DICT, render intents. New dependencies rdflib, pyshacl, jsonschema. **Rendered text changes.**
- **6.2.38** (#590): DCAT Catalog runs with a search string; My Egeria domain selection passes the GUID. Tagged, not published to PyPI.
- **6.2.39** (#591): Dr.Egeria keeps one list item per bullet (behaviour change for "- a, b"); carries the 6.2.38 fixes.

### Fixed in 6.2.36, for reference
- **ISSUE-185**: `get_collection_members` paging; `saved_query` counts distinct elements; folder walks now page every folder.
- **Behaviour change**: with `body=` and no paging, the method's `page_size` default now applies. This affects 19 methods.

---

# Appendix: detailed lists

## A. trellis (`dwolfson/trellis#N`)

### Highlights
- Shared feedback library with a closed loop (dwolfson/trellis#1012, #1018, #1019, #1031).
- Re-index with swap, rebuild and rollback (dwolfson/trellis#1038, #1053, #1054).
- Publish to Egeria with zoning and read-back; engine-host surveys with cancel (dwolfson/trellis#644, #729, #735).
- Database quality checks and value profile (dwolfson/trellis#767, #816, #894).
- Egeria Advisor security hardening and dashboards parity (dwolfson/trellis#1045, #1046, #1067, #1068).
- New UI looks and cards/tiles (dwolfson/trellis#765, #776, #1062).

### New
- Cards and tiles in the Next UI (C1): components, tokens, At a glance, Survey & analyses (dwolfson/trellis#776, #778, #782).
- Look control: Dark, Light, Paper (dwolfson/trellis#765); every data table resizes (dwolfson/trellis#942).
- Generic graph renderer; deployment topology first (dwolfson/trellis#831).
- Markdown rendering in the chat rail and journal preview (dwolfson/trellis#855, #861).
- Per-table heap and index sizes (dwolfson/trellis#582); database survey flags, materialized views, activity (dwolfson/trellis#627).
- One card per Survey Definition with run line, history, Cancel (dwolfson/trellis#729, #735).
- Engine-host steps and two staleness measures (dwolfson/trellis#658, #663, #699).
- OpenLineage run event per step (dwolfson/trellis#646).
- Value profile and quality checks: sampling settings at every scope, column-profile verdicts kept locally, Publish sends them, quality survey across a work list on a schedule (dwolfson/trellis#759, #767, #772, #880, #893, #894).
- schema_comparison set step (dwolfson/trellis#952); a set steps section on work-list pages (dwolfson/trellis#944).
- Declared extensibility slices: declaration, Curate publish table, a step's new questions (dwolfson/trellis#885, #886, #916, #919).
- Files: Egeria's CSV survey read, Parquet profile and Delta Lake signal, narrative passages searched by chat (dwolfson/trellis#868, #912, #977).
- Open data: publish one dataset with read-back (OD4), DOI-only repository states what is established (dwolfson/trellis#946, #982).
- Locator screen and chat citations on screen (dwolfson/trellis#913).
- Chat: first index asked with per-repository consent; Ollama native endpoint; Phoenix tracing (dwolfson/trellis#777, #779, #745).
- Tutorial parts 1 to 6 (dwolfson/trellis#969, #970, #972, #975, #983, #990).
- trellis-feedback 0.1 to 0.3; RE feedback adoption, closed loop steps 1 to 2c (dwolfson/trellis#1012, #1013, #1017, #1018, #1019, #1031, #1032, #1034).
- Compile: as-of date on every evidence section (dwolfson/trellis#1021, #1024).
- Re-index R0, R1a to R1c, R2 (dwolfson/trellis#1037, #1038, #1039, #1040, #1041).
- trellis-ui (A-U3) and trellis-accel (WIP) (dwolfson/trellis#1062, #1073).
- EA: Admin link, `is_admin`, dashboards read/author/parity, used-by display names, feedback library (dwolfson/trellis#1050, #1052, #1042, #1067, #1068, #1069, #1070).
- RE: catalog resource type and Egeria Overview questions as rows (dwolfson/trellis#1002).

### Fixed
- Identity and access: ambient identity, caller identity rounds, private investigation attach, no forged person actions from the CLI, constant-time token compare, non-JWT tokens refused, dead token answered the same everywhere, zone with no control is private (dwolfson/trellis#579, #587, #640, #665, #685, #827, #997, #1043).
- Credentials only via the secrets store (dwolfson/trellis#823); short password never corrupts the publish word (dwolfson/trellis#621).
- Honest results: unsurveyed database is not established, "not determined" never reads 0, a partial failure on a reused report is a failure, capped list says it is capped (dwolfson/trellis#616, #625, #783, #769).
- Publish: link ExternalReference/LineageMapping once, never on re-publish; membership read-back pages (dwolfson/trellis#678, #682, #631).
- Work lists: refused add is not "maybe attached"; publish never hands the drain a blank lookup (dwolfson/trellis#632, #633).
- Heal verifies Egeria, not its ledger (dwolfson/trellis#1003); foundations stops creating the content pack's Perspectives (dwolfson/trellis#1007).
- Chat: engine-less session handling, views excluded from table counts, scoped question naming another resource asks which (dwolfson/trellis#744, #746, #643).
- PostgreSQL temporary schemas excluded from schema count (dwolfson/trellis#973).
- Static files answer no-cache (dwolfson/trellis#998).
- EA: feedback no longer blocks the event loop; Dr.Egeria runs as the signed-in user; no-credential calls refused; strict mermaid; throwaway test schema (dwolfson/trellis#1044, #1045, #1046, #1047, #1051).
- EA runtime image includes trellis-feedback (dwolfson/trellis#1074).
- EA: an Egeria 5xx or a dropped connection at Portal sign-in is reported as "unreachable", not "rejected" (dwolfson/trellis#1077).
- EA feedback: a changed vote supersedes the earlier one for that answer; the recorded intent is the one the question was routed to, not the selector (dwolfson/trellis#1078).
- Rebuild refuses only a PDF regression; Docling on CPU instead of Apple MPS (dwolfson/trellis#1058, #1055).
- Open-data connect errors say what to do (dwolfson/trellis#1009).

### Changed / behaviour changes
- Retired the plaintext DB credential fallback (dwolfson/trellis#823).
- Reports say "published" rather than the old not-yet-published wording (dwolfson/trellis#618, #619).
- A held rebuild is "held", not done; admins can cancel (dwolfson/trellis#1053, #1054).
- A private context keeps the question in Admin until explicitly re-routed (dwolfson/trellis#1031).
- Private resources never offer an Egeria-dispatched survey (dwolfson/trellis#991).
- Look: Paper kept for one release alongside the Portal's Dark and Light (dwolfson/trellis#763).

### Dependencies
- pyegeria floor raised from 6.1.15 to 6.2.1, then step by step to 6.2.39 (dwolfson/trellis#593, #651, #728, #806, #819, #834, #853, #951, #959, #974, #987, #1005, #1028, #1036, #1061, #1071, #1076, #1082, #1083).
- certifi floor excludes the emSign ECC G3 root (dwolfson/trellis#989).
- Analytic Library from PyPI: `egeria-trellis-analytics` 0.2.0 (dwolfson/trellis#996).
- About 20 odpi-side Dependabot bumps (notebook, jupyterlab, mlflow, aiohttp, authlib, pypdf and others) via the sync (dwolfson/trellis#112).

### Ops/CI
- CI: RE tests on main and PRs only; job timeout raised to 60, then 90 minutes; stale image runs cancelled; PR images only when inputs change; ea-tests cover querycache (dwolfson/trellis#884, #601, #891, #670, #1075, #1063).
- Tests: no tracked files written, ratchets for silent success, pyegeria contract test (dwolfson/trellis#595, #1048, #1056).
- Dr.Egeria templates synced (dwolfson/trellis#91, #103, #104, #639, #858, #874, #1004).
- Odpi sync and DCO remediation (dwolfson/trellis#108, #981, #112).

### Docs
- Tutorial parts 1 to 6; user and admin guide rounds; design-note reorganisation into exchange/implemented/rulings (dwolfson/trellis#683, #688, #695, #969, #970, #972).
- Design notes: Files, open data, quality, extensibility, local dashboards, OSI metric exchange, feedback extraction, closed loop, re-index, hardware acceleration (dwolfson/trellis#785, #786, #889, #939, #978, #984, #1011, #1016, #1035, #1072).

## B. pyegeria

Per-release detail is in the themes above; the appendix is the same list by section.

### New
- Report specs held in Egeria; consumer folders; restricted specs (6.2.28, 6.2.33, 6.2.35).
- Egeria 6.3 report specs, measurements and dashboards client and Dr.Egeria commands (6.2.24).
- Dashboard Sheets in Egeria with owner and folders (6.2.31, 6.2.34).
- Analytic registry declarations and resolution (6.2.16 to 6.2.18, 6.2.24, 6.2.25).
- Dr.Egeria: Business Capability, statement of applicability, survey report, security findings, Reference Data (6.2.3, 6.2.11 to 6.2.13).
- Security annotation models and findings/posture reports (6.2.13).
- Governance Engine client for the engine-action operations Egeria moved (6.2.5).
- DOCUMENT output, DCAT Catalog export, structured TABLE and native DICT (6.2.37).

### Fixed
- Five update methods that sent no body (6.2.7); fields silently dropped SDK-wide (6.2.10); link/detach reporting success without sending (6.2.28); caller token re-authentication (6.2.15); collection and folder paging (6.2.36); DCAT Catalog by search string, My Egeria domain GUID (6.2.38).

### Changed / behaviour changes
- `population=` replaces `scope=` (6.2.24); unmeasured is `None`, not 0 (6.2.22); absence word `nothing_found` (6.2.23); a failed bearer-token request now raises (6.2.13); `page_size` default now applies with `body=` and no paging on 19 methods (6.2.36); 403 not 401 (6.2.34); rendered text changes (6.2.37); one list item per bullet (6.2.39).

### Dependencies
- certifi floor and tornado 6.6 (6.2.21); codeql-action and action-gh-release bumps; multidict 6.9.1.

### Ops/CI
- Release process: 39 tagged releases (6.2.38 not published to PyPI); Scorecard workflow fix.

### Docs
- Issue tracker brought up to date and re-sorted in several passes; analytic function resolution documented (ISSUE-169 to ISSUE-172).

## C. egeria-workspaces (`odpi/egeria-workspaces#N`)
<!-- Candidate at the cut (2026-11-16): sample statements of applicability for Coco (#881, merged 38c999a6); Egeria Explorer Statements of Applicability view (#882, NOT merged yet; include only if it merges before the cut). -->

### Highlights
- Dashboards and report specs held in Egeria, by folder, with Used by (odpi/egeria-workspaces#818, #821, #826, #829, #830).
- Overview shows only what it measured (odpi/egeria-workspaces#783, #785, #790, #807).
- Relationship purpose families, resizable widths (odpi/egeria-workspaces#752, #753, #754).
- Resource Browser (odpi/egeria-workspaces#620 to #625).
- Public demo hardening and loopback-only ports (odpi/egeria-workspaces#640, #642, #644).
- New tutorials and worked examples (odpi/egeria-workspaces#825).

### New
- Local Dashboards: Egeria-held sheets by folder with Used by (#830); folder tree and memberships (#829); four useful sheets and trend tiles (#826); dashboards held in Egeria, token-only API (#818); Report tiles pin collections by qualifiedName (#824); result and sheet caches (#814, #815).
- Report specs: declarations, resolution, refusals (#809); inputs supplied by role (#806); consumer folders and Used by chips (#821).
- Portal Insights saved queries refresh (#823); Collections grouped by type (#816, #817).
- Overview: Trellis perspectives, `asset_composition`, background measurement (#788, #793, #790).
- Mermaid Expand viewer (#781).
- Classifications grouped by classification purpose (#831); one renderer for pyegeria's structured TABLE (#855, #856); result notes under every result (#852); DCAT support and an OpenLineage log store notebook (#849, #847); `egeria-upgrade-reset` with a shared-infra health check and a last-reset panel (#851, #854); hand-run seeds heal after a reset (#850).
- Relationship purposes, Type Explorer inheritance, Data Mesh link and property columns (#752, #753, #756, #775, #774).
- Resizable widths (#754).
- Lineage Explorer hop limit and cut markers (#749).
- Catalog: Infrastructure tabs, View buttons, filter and sort (#693, #709, #656, #657).
- Resource Browser phases 1 to 3 and contents view (#620, #621, #622, #625); Curation Coverage tile (#628).
- Notebooks in data initialization (#662, #685); usage workload batch (#684).
- Demo: Airflow and Marquez with lineage to Egeria (#706); `--lan` (#687); egress allow-list (#733); evict stuck workbench (#739); 2-hour tokens (#651); Pasteur nanny (#822); Pepys (#636).
- Egeria Advisor service account (#828); Phoenix compose (#645); TestGen runtime (#663); Governance Engine view service (#639).
- Coco content: CDO dashboard (#780), security, sustainability, resilient loading (#691, #692, #698, #702), Airflow DAGs (#653), system data layer (#660).
- Dr.Egeria templates: Security Officer, Business Capability, report-spec/dashboard, Postgres secrets, pyegeria syncs (#703, #694, #803, #679, #711, #623, #730).
- Bootstrap: recursive batches, per-file run-as user (#618); heal primes valid metadata (#801).

### Fixed
- Credential leak: platform-URL allowlist (#819); service-user impersonation (#715); `/api/types` routes no longer take `user_id` (#831).
- Local Dashboards: tables capped at whole rows with the real scope (#848), scroll in their tile (#833), `<br>` in cells (#846); The Catalog no longer blanks without saved connection settings (#832); Marquez restarts after a reboot (#857).
- Overview honesty fixes (#783, #807, #791, #755).
- Extended properties, duplicate relationships, map-valued properties (#699, #700, #701, #682).
- Catalog lists page to the end; Data Assets tree; list caches (#659, #658, #661, #666).
- Blank Data Mesh/Locator pages; text contrast (#654, #655).
- Type Explorer fixes (#777, #750, #745, #746); solution components (#716, #717).
- ISC graphs on Egeria 6.3 and 404 for missing ISC (#710, #648).
- Jupyter distrusts emSign G3 (#776); Obsidian lock-down and demo hardening (#640, #642, #643); MCP SSE headers (#738).
- Demo reset (#646, #729); shared infra (#624, #686, #820); loading bay Bitol folder (#681); secrets refresh (#638); empty limits (#641); compose build (#626).

### Changed / behaviour changes
- Ports bind to 127.0.0.1 by default (#644, #687).
- 2-hour bearer tokens (#651).
- `presentationStyle` replaces `emphasis`; MeasurementSpecification references become relationships (docs: #796, #795).
- Egeria 6.3-SNAPSHOT platform pins through the Pasteur build (#647, #748, #740, #798, #800, #805, #808, #810, #827); freshstart pyegeria capped below 6.2.27 (#807).
  <!-- TODO (Coordinator, 2026-11-14): laz platform upgrade ~20:45Z brings odpi/egeria#9453 (paging contract) and odpi/egeria#9450 (Wedgwood subscription performance). Upgrade done (platform 5deda38d). Coordinator's laz check: #9453 fixed paging for finds and property-value lookups; relationship-by-type retrieval still ends early when filtering empties a page (reported to the owner; keep this a known issue unless fixed by the cut). 2026-11-15: image-only upgrade 5deda38d → a5c3a195 (odpi/egeria main c61bad65, adds odpi/egeria#9454; describe from the upstream PR). Cite the workspaces pin PR when it lands; describe both for users from the upstream PRs, not from this note. -->
- Analytic functions and metric paths by registered name (#741, #742, #743, #811).
- Postgres templates take a secrets store (#679).

### Dependencies
- pyegeria floor 6.2.7 up to 6.2.24; the images run newer (#667, #680, #688, #695, #707, #712, #731, #736, #751, #772, #789, #802).
- Dependabot and consolidated bumps (dagster, playwright, Airflow, openlineage, confluent-kafka, mcp, schemathesis, pytest, python base images, prefect, certbot, docker) (#652, #708, #718, #737, #757 to #771).
- Obsidian plugin dependency fixes (#704); Dependabot ignore rules (#768).

### Ops/CI
- Actions bumps: checkout 7, upload-artifact 7, codeql 4.38.2, scorecard 2.5.0, claude-code-action 1.0.266 (#542, #543, #596, #764, #765).
- Shared Postgres tuning and `pg_stat_statements`; Airflow lineage to Egeria only (#686, #784, #804).
- Heap dump on out-of-memory (#773); deltalake-spark updates (#744, #747); `.claude/` ignored (#779).

### Docs
- Tutorials for saved queries, analytic functions, report specs, local dashboards (#825, #728).
- Portal Docs reorganisation; Resource Locator guide; notebooks in data initialization (#728, #649, #664).
- Report-spec design notes and Portal behaviour (#778, #782, #786, #787, #792, #794, #799, #813, #683, #797).
- `RELEASE_NOTES.md` is written per release; update it at release time.
