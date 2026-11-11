<!-- DRAFT: new file RELEASE_NOTES.md at the root of dwolfson/trellis, mirroring egeria-workspaces' RELEASE_NOTES.md.
     Range b74b07f9 (2026-10-09) to c9892ec2 (#1078, 2026-11-11). Refresh the stats at the cut.
     TODO (owner): release label (see the CHANGELOG draft's note); whether RE and EA are reachable on the public demo
     (the "Try it" list assumes not, and points at running them with the quickstart). -->

# Trellis 6.3: Resource Explorer and Egeria Advisor

Five weeks, about 500 merged PRs, and two early previews that now publish to Egeria, run their surveys through it,
and learn from the people who use them.

In the October 2026 Egeria newsletter, Resource Explorer and Egeria Advisor were "early previews". Since then the
work has been about three things: putting what Resource Explorer finds **into Egeria** (published, zoned, read back,
and surveyed by Egeria's own engine host); making every answer say **what it established and what it did not**; and
**closing the loop** with the people who use it, through shared feedback, triage and a document index that can be
rebuilt and rolled back. Egeria Advisor now reads and authors the same Egeria-held dashboards and report specs as the
Portal. It ships with **Egeria 6.3** and requires **pyegeria 6.2.36**.

**6.3** &middot; **1,140** commits &middot; **~515** PRs &middot; **12** packages &middot; **5** weeks

## Try it

- **Run it with Egeria Workspaces**: [Deploying Trellis with the QuickStart](docs/deploying-trellis-with-quickstart.md)
  and [QUICKSTART.md](QUICKSTART.md). Both applications open from tiles on the Egeria Workspaces Portal home page.
- **Learn Resource Explorer**: the six-part [tutorial](packages/resource-explorer/docs/tutorial/).
- **Understand the design**: [Trellis architecture](docs/trellis-architecture.md) and [the journey so far](docs/trellis-journey.md).

---

## Mid Oct: publish to Egeria, surveys by Egeria, and whose identity

- **Publish to Egeria with zoning and read-back** (#644 and follow-ups). Resource Explorer zones what it produced,
  never what it references; private material publishes only as its owner and fails closed; links such as
  ExternalReference and LineageMapping are made once, never again on re-publish (#678, #682); membership read-back pages (#631).
- **Engine-host surveys**: steps run by Egeria's engine host with two staleness measures (#658, #663, #699), and an
  OpenLineage run event for every step (#646).
- **Database surveys** gain per-table heap and index sizes (#582), flags, materialized views and activity (#627).
- **Identity**: ambient identity and caller-identity rounds (#579, #587), private investigation attach (#640), no
  forged person actions from the CLI (#665), constant-time token compare (#685).
- **Honest results**: an unsurveyed database is "not established"; "not determined" never reads 0 (#616, #625).

## Late Oct: a new interface, quality checks, files, and a better chat

- **Next UI**: cards and tiles, At a glance, Survey & analyses (#776, #778, #782); the Look control (Dark, Light,
  Paper) (#765); a generic graph renderer, deployment topology first (#831); every data table resizes (#942).
- **Value profile and quality checks**, with sampling settings at every scope; verdicts are kept locally and sent to
  Egeria by Publish; a quality survey runs across a work list on a schedule (#759, #767, #772, #880, #893, #894).
- **One card per Survey Definition** with a run line, history and Cancel (#729, #735).
- **Chat**: the first index of a repository is asked about first (#777); Ollama native endpoint (#779); Phoenix
  tracing (#745); markdown in the chat rail and journal preview (#855, #861).
- **Credentials only through the secrets store**; the plaintext fallback is retired (#823). Non-JWT tokens are refused
  at login (#827).
- **Files**: Egeria's CSV survey, Parquet profile, Delta Lake layout signal, and narrative passages that chat can search
  (#868, #912, #977). **Declared extensibility**: a step declares itself and the questions it adds (#885, #886, #916, #919).

## Early Nov: tutorial, open data, and the Analytic Library on PyPI

- **Tutorial parts 1 to 6**, from what Resource Explorer is for to analysis further down the funnel
  (#969, #970, #972, #975, #983, #990).
- **Open data**: publish one dataset with read-back (#946); a DOI-only repository states what is established (#982).
- **Set steps**: `schema_comparison` (#952) and a set-steps section on work-list pages (#944).
- **The Analytic Library is a published wheel**, `egeria-trellis-analytics` 0.2.0 (#996).
- **A zone with no access control is private**, matching Egeria (#1043); a dead token is answered the same way
  everywhere (#997); the certifi floor excludes the emSign ECC G3 root (#989).

## Nov 8–11: closing the loop, and Egeria Advisor on Egeria-held dashboards

- **`trellis-feedback`**, a shared feedback library (0.1 to 0.3): ratings carry a cause and evidence, an admin triages
  them, and a diagnosis can be routed to a gap in the documents (#1012, #1013, #1017, #1018, #1019, #1031, #1032, #1034).
- **Re-index**: the document index can be rebuilt, swapped in and rolled back; a held rebuild says "held", and admins
  can cancel it (#1037 to #1041, #1053, #1054).
- **Evidence has an as-of date** on every compiled section (#1021, #1024).
- **Egeria Advisor**: Dashboards read and authored in Egeria, at parity with the Portal (#1042, #1067, #1068, #1070);
  report specs synced from, published to and withdrawn from Egeria (#1033, #1060); perspectives from Egeria (#1059);
  one fail-closed admin gate (#1050, #1052); Dr.Egeria runs as the signed-in user and calls with no credentials are
  refused (#1045, #1046); feedback through the shared library (#1069, #1078); Egeria being down at sign-in is
  "unreachable", not "rejected" (#1077).
- **`trellis-ui`** (#1062) and **`trellis-accel`**, choosing a compute device at run time, work in progress
  (#1073; design #1072).

## Underneath all of it

- **pyegeria** floor from 6.1.15 to 6.2.36 in sixteen steps (#593 … #1076).
- **CI**: Resource Explorer tests run on main and PRs; image builds only when their inputs change (#1075); tests write
  no tracked files and ratchet against silent success (#595, #1048); a pyegeria contract test (#1056).
- **Docs**: user and admin guides, and design notes for files, open data, quality, extensibility, local dashboards,
  OSI metric exchange, feedback, re-index and hardware acceleration.

**Commits by author:** 1,125 — Dan Wolfson &middot; 16 — dependabot[bot]

---

## Upgrade notes

- **pyegeria 6.2.36 or later is required** by Resource Explorer and Egeria Advisor (#1076).
- **Database credentials must be in the secrets store.** The plaintext fallback is gone (#823).
- **Only JWT bearer tokens are accepted at login** (#827).
- **Zones**: a zone with no access control is private, as in Egeria (#1043). Content in such zones is visible only to
  its owner.
- **Private resources** no longer offer an Egeria-dispatched survey (#991).
- **The Analytic Library comes from PyPI** (`egeria-trellis-analytics` 0.2.0) instead of the in-repo package (#996).
- **Egeria Advisor runs as its own service account**, `egeriaadvisornpa`, in the Egeria Workspaces quickstart
  (odpi/egeria-workspaces#828).

## Where the detail lives

The full list by section is in [CHANGELOG.md](CHANGELOG.md). Design notes are under `docs/`.

*trellis 6.3 &middot; b74b07f9 (2026-10-09) → 6.3 &middot; compiled from git history*
