<!-- DRAFT: new file CHANGELOG.md at the root of dwolfson/trellis.
     Baseline b74b07f9 (2026-10-09, the October 2026 newsletter) to 73738df8 (#1086, 2026-11-12).
     Owner decision 2026-11-11: the release is "6.3 Tech Preview", tagged and released (GitHub release) to coincide
     with the Egeria 6.3 release, tentatively Monday 2026-11-16. Tag name: v6.3-tech-preview (owner, 2026-11-13).
     Package versions (resource-explorer 0.1.0, egeria-advisor 0.1.2, ...) are left as they are. -->

# Changelog

All notable changes to this repository (Resource Explorer, Egeria Advisor and the shared `trellis-*` packages)
are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Releases are named after the
Egeria release they ship with. Pull requests are `#N` in this repository.

## [Unreleased]

## [6.3 Tech Preview] - 2026-11-16

First recorded release, a Tech Preview released with Egeria 6.3. It covers everything merged since the October 2026 Egeria newsletter, which introduced
Resource Explorer and Egeria Advisor as early previews. See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the narrative.

### Added

#### Resource Explorer
- **Publish to Egeria** with read-back and zoning: what Resource Explorer produced is zoned, never what it references;
  private members publish only as their owner; a Publish button with plain-language failures (#644; see PRs for
  follow-ups).
- **Surveys run by Egeria's engine host**: one card per Survey Definition with a run line, history and Cancel
  (#729, #735); engine-host steps and two staleness measures (#658, #663, #699); an OpenLineage run event per step (#646).
- **Database analysis**: per-table heap and index sizes (#582); survey flags, materialized views and activity (#627);
  value profiles and quality checks with sampling settings at every scope, column-profile verdicts kept locally and
  sent by Publish, and a scheduled quality survey across a work list (#759, #767, #772, #880, #893, #894).
- **Set steps**: a `schema_comparison` step (#952) and a set-steps section on work-list pages (#944).
- **Declared extensibility**: a step's declaration, the Curate publish table and the new questions a step adds
  (#885, #886, #916, #919).
- **Files**: Egeria's CSV survey read, Parquet profile and Delta Lake layout signal, narrative passages searched by chat
  (#868, #912, #977).
- **Open data**: publish one dataset with read-back (#946); a DOI-only repository states what is established (#982).
- **Locator screen** and chat citations on screen (#913); catalog resource type, and Egeria Overview questions as rows (#1002).
- **Chat**: the first index of a repository is asked about first, with per-repository consent (#777); Ollama native
  endpoint (#779); Phoenix tracing (#745); markdown rendering in the chat rail and journal preview (#855, #861).
- **Compile**: an as-of date on every evidence section (#1021, #1024).
- **Next UI**: cards and tiles with At a glance and Survey & analyses (#776, #778, #782); a Look control with Dark, Light
  and Paper (#765); every data table resizes (#942); a generic graph renderer, deployment topology first (#831).
- **Tutorial** parts 1 to 6 (#969, #970, #972, #975, #983, #990).
- **Feedback with a closed loop** using `trellis-feedback`: ratings carry a cause and evidence, admin triage, a
  diagnosis can be routed to a gap (#1012, #1013, #1017, #1018, #1019, #1031, #1032, #1034).
- **Re-index**: rebuild, swap and roll back the document index (#1037, #1038, #1039, #1040, #1041).

#### Egeria Advisor
- **Dashboards in Egeria**: lists and shows Egeria-held sheets as the signed-in user (#1042), then reads and authors
  them at parity with the Portal (#1067, #1068); Used by shows display names (#1070);
  large tables scroll inside their tile and a capped table says what it left out (#1084); an unreadable or empty
  folder says why (#1086).
- **Report specs in Egeria**: syncs report specs held in Egeria, retiring the Phase-1 loader (#1033); publishes and
  withdraws specs, restricted per user, with Used by (#1060).
- **Perspectives from Egeria**, with an absence that says why (#1059).
- **One fail-closed admin gate** from `trellis-auth` (#1050); the Admin link is shown only to admins (#1052).
- **Feedback** through the shared `trellis-feedback` library (#1069).

#### Shared packages
- **`trellis-feedback`** 0.1 to 0.3: a shared feedback store with append-only triage (#1012 onwards).
- **`trellis-ui`**, a shared UI package; Egeria Advisor gets the three looks (#1062).
- **`trellis-accel`**, choosing a compute device at run time; work in progress (#1073; design note #1072).
- **The Analytic Library moved out** as `egeria-trellis-analytics` 0.2.0 on PyPI (#996).

### Changed
- The plaintext database-credential fallback is retired; credentials come only from the secrets store (#823).
- Reports say "published" rather than the old not-yet-published wording (#618, #619).
- A held rebuild is "held", not done, and admins can cancel it (#1053, #1054).
- A private context keeps its question in Admin until it is explicitly re-routed (#1031).
- Private resources never offer an Egeria-dispatched survey (#991).
- The Paper look is kept for one release alongside the Portal's Dark and Light (#763).
- A zone with no access control is private, matching Egeria (#1043).
- Egeria Advisor feedback: a changed vote supersedes the earlier one for that answer, and the recorded intent is the
  one the question was routed to rather than the selector (#1078).
- Egeria Advisor drops its unread `EMBEDDING_DEVICE` setting (#1080).

### Fixed
- **Identity and access**: ambient identity, caller-identity rounds, private investigation attach, no forged person
  actions from the CLI, constant-time token compare, non-JWT tokens refused at login, a dead token answered the same
  way everywhere (#579, #587, #640, #665, #685, #827, #997).
- A short password never corrupts the publish word (#621).
- **Honest results**: an unsurveyed database is "not established"; "not determined" never reads 0; a partial failure
  on a reused report is a failure; a capped list says it is capped (#616, #625, #783, #769).
- **Publish**: ExternalReference and LineageMapping are linked once, never again on re-publish; membership read-back
  pages (#678, #682, #631).
- **Work lists**: a refused add is not "maybe attached"; Publish never hands the drain a blank lookup (#632, #633).
- Heal verifies Egeria, not its own ledger (#1003); foundations no longer creates the content pack's Perspectives (#1007).
- **Chat**: engine-less sessions, views excluded from table counts, a scoped question that names another resource
  asks which one (#744, #746, #643).
- PostgreSQL temporary schemas are excluded from the schema count (#973).
- Static files are served no-cache (#998).
- Open-data connection errors say what to do (#1009).
- Rebuild refuses only a PDF regression (#1058); Docling runs on CPU instead of Apple MPS (#1055).
- **Egeria Advisor**: feedback no longer blocks the event loop (#1044); Dr.Egeria runs as the signed-in user (#1045);
  calls with neither token nor password are refused (#1046); strict mermaid rendering (#1047); throwaway test schema
  (#1051); the runtime image includes `trellis-feedback` (#1074); an Egeria 5xx or a dropped connection at Portal
  sign-in is "unreachable", not "rejected" (#1077); a saved-query count tile shows no member table under the
  number (#1081).

### Security
- See *Fixed › Identity and access* and *Changed* (credential fallback retired, zone rule).
- The certifi floor excludes the distrusted emSign ECC G3 root (#989).

### Dependencies
- pyegeria floor raised from 6.1.15 to 6.2.1, then step by step to 6.2.41 (#593, #651, #728, #806, #819, #834, #853,
  #951, #959, #974, #987, #1005, #1028, #1036, #1061, #1071, #1076, #1082, #1083; TODO: add the 6.2.41 floor PR at the cut).
- About 20 Dependabot bumps from the odpi side (notebook, jupyterlab, mlflow, aiohttp, authlib, pypdf and others),
  via the sync (#112).

### CI and tests
- Resource Explorer tests on main and PRs only; job timeout raised to 60, then 90 minutes; stale image runs cancelled;
  PR images built only when their inputs change; ea-tests cover querycache; builder and runtime image stages copy the same workspace packages
  (#884, #601, #891, #670, #1075, #1063, #1079).
- Tests write no tracked files; ratchets for silent success; a pyegeria contract test; the spec-sync fake answers an
  empty page the way Egeria does (#595, #1048, #1056, #1085).
- Dr.Egeria templates synced (#91, #103, #104, #639, #858, #874, #1004); odpi sync and DCO remediation (#108, #981, #112).

### Docs
- User and admin guide rounds; design notes reorganised into exchange, implemented and rulings (#683, #688, #695).
- Design notes: files, open data, quality, extensibility, local dashboards, OSI metric exchange, feedback extraction,
  closed loop, re-index, hardware acceleration (#785, #786, #889, #939, #978, #984, #1011, #1016, #1035, #1072).

[Unreleased]: https://github.com/dwolfson/trellis/compare/v6.3-tech-preview...HEAD
[6.3 Tech Preview]: https://github.com/dwolfson/trellis/compare/b74b07f9...v6.3-tech-preview
