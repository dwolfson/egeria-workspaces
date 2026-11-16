<!-- DRAFT: new top section for odpi/egeria-workspaces RELEASE_NOTES.md.
     At release: put this above "# Egeria Workspaces 6.2", demote 6.2's H1 if the file should hold several
     releases, and REMOVE the 6.2 file's "## Since 6.2 (unreleased, on main)" section (folded in below).
     Move 6.2's "Report specs held in Egeria are read from the Portal's consumer folder" upgrade note here
     (it describes 6.3 behaviour). Stats are from 903e8eeb (#619, 2026-10-09) to 3b8ac7e2 (#857, 2026-11-12);
     refresh them at the cut. Release tentatively Monday 2026-11-16, alongside Egeria 6.3 (owner, 2026-11-11);
     v6.2 is tagged at 903e8eeb. These notes are also our piece of the Egeria project's 6.3 release notes.
     Resource Explorer and Egeria Advisor ship as the "6.3 Tech Preview" (dwolfson/trellis). -->

# Egeria Workspaces 6.3

Since the 6.2 release on October 9, our work on `egeria-workspaces` has focused on:

* Keeping up with the new features in Egeria, and making them easy to reach and to observe.
* Extending reports and dashboards into Egeria, while still letting users and teams create and manage
  their own local ones.
* Improving the accuracy and transparency of the measurements, metrics and KPIs we display.

This release goes with **Egeria 6.3** and needs **pyegeria 6.2.42 or later**; we recommend **pyegeria 6.3.0**, the release that matches Egeria 6.3.<!-- When the 6.3 bundle raises the code floors to 6.3.0, say "pyegeria 6.3.0 or later" and cite the bundle PR. --> For the changes to the Egeria
platform itself, see the [Egeria 6.3 release notes](https://egeria-project.org/release-notes/latest/) and the
[November 2026 newsletter](https://egeria-project.org/release-notes/november-2026/).

In numbers: 377 commits and 217 merged pull requests over five weeks.

## Try it

- **Live demo**: you can try everything at [egeria.pdr-associates.com](https://egeria.pdr-associates.com)
  without installing anything. Register for free, pick a Coco Pharmaceuticals persona, and explore. Open
  **Local Dashboards** to see the dashboard sheets held in Egeria, organized by folder.
- **Run it yourself**: follow [Getting started](https://github.com/odpi/egeria-workspaces#getting-started) to
  run Quickstart or Freshstart locally with Docker or Podman. Add `--lan` if you want to reach it from other
  machines.
- **Learn by doing**: new [Portal tutorials](portal-docs/tutorials/overview.md) cover saved queries, analytic
  functions, report specs and local dashboards, with [worked examples](portal-docs/tutorials/worked-examples.md).

---

## Mid October: the Resource Browser and a more secure demo

- **Resource Browser** ([#620](https://github.com/odpi/egeria-workspaces/pull/620),
  [#621](https://github.com/odpi/egeria-workspaces/pull/621), [#622](https://github.com/odpi/egeria-workspaces/pull/622),
  [#625](https://github.com/odpi/egeria-workspaces/pull/625)): a page per resource with what it contains, its
  meaning and notes on its parts; search, home and browse; work lists and team sharing. Resource Explorer's
  **Curation Coverage** appears as a Dashboard Sheet tile ([#628](https://github.com/odpi/egeria-workspaces/pull/628)).
- **We continue to harden the Portal environment** ([#640](https://github.com/odpi/egeria-workspaces/pull/640),
  [#642](https://github.com/odpi/egeria-workspaces/pull/642), [#643](https://github.com/odpi/egeria-workspaces/pull/643)).
- **Ports bind to `127.0.0.1` by default** ([#644](https://github.com/odpi/egeria-workspaces/pull/644)); bearer
  tokens last two hours ([#651](https://github.com/odpi/egeria-workspaces/pull/651)).
- The Governance Engine view service ([#639](https://github.com/odpi/egeria-workspaces/pull/639)), the Phoenix
  compose ([#645](https://github.com/odpi/egeria-workspaces/pull/645)) and the first Egeria 6.3-SNAPSHOT platform
  pin ([#647](https://github.com/odpi/egeria-workspaces/pull/647)).
- **The Catalog** gains filter and sort on long lists and tables ([#656](https://github.com/odpi/egeria-workspaces/pull/656),
  [#657](https://github.com/odpi/egeria-workspaces/pull/657)); every list pages to the end and Data Assets show
  every type as a tree ([#658](https://github.com/odpi/egeria-workspaces/pull/658),
  [#659](https://github.com/odpi/egeria-workspaces/pull/659), [#661](https://github.com/odpi/egeria-workspaces/pull/661),
  [#666](https://github.com/odpi/egeria-workspaces/pull/666)); blank Data Mesh and Locator pages fixed
  ([#654](https://github.com/odpi/egeria-workspaces/pull/654), [#655](https://github.com/odpi/egeria-workspaces/pull/655)).
- **Data initialization can run notebooks** ([#662](https://github.com/odpi/egeria-workspaces/pull/662)).

## Late October: lineage from Airflow, more Coco content, and credential fixes

- **Airflow and Marquez start with the demo**, and Airflow's OpenLineage events reach Egeria as well as Marquez
  ([#706](https://github.com/odpi/egeria-workspaces/pull/706)); `--lan` opens the ports for one run
  ([#687](https://github.com/odpi/egeria-workspaces/pull/687)).
- **Coco Pharmaceuticals content**: security support, sustainability reference data and more resilient batch
  loading ([#691](https://github.com/odpi/egeria-workspaces/pull/691), [#692](https://github.com/odpi/egeria-workspaces/pull/692),
  [#698](https://github.com/odpi/egeria-workspaces/pull/698), [#702](https://github.com/odpi/egeria-workspaces/pull/702));
  Airflow DAGs and a system data layer ([#653](https://github.com/odpi/egeria-workspaces/pull/653),
  [#660](https://github.com/odpi/egeria-workspaces/pull/660)); a usage workload batch
  ([#684](https://github.com/odpi/egeria-workspaces/pull/684)).
- **Dr.Egeria templates** for the Security Officer and Business Capability commands, and Postgres templates
  that take a secrets store ([#703](https://github.com/odpi/egeria-workspaces/pull/703),
  [#694](https://github.com/odpi/egeria-workspaces/pull/694), [#679](https://github.com/odpi/egeria-workspaces/pull/679)).
- **The Catalog's Infrastructure section** has a tab per subtype ([#693](https://github.com/odpi/egeria-workspaces/pull/693)),
  and schema rows get View buttons ([#709](https://github.com/odpi/egeria-workspaces/pull/709)); extended properties, map-valued properties and
  duplicate relationship cards fixed ([#699](https://github.com/odpi/egeria-workspaces/pull/699),
  [#700](https://github.com/odpi/egeria-workspaces/pull/700), [#701](https://github.com/odpi/egeria-workspaces/pull/701),
  [#682](https://github.com/odpi/egeria-workspaces/pull/682)).
- **Security**: a signed-in user's request is no longer run as the service user
  ([#715](https://github.com/odpi/egeria-workspaces/pull/715)); workbenches sit behind an egress allow-list
  ([#733](https://github.com/odpi/egeria-workspaces/pull/733)); MCP SSE headers fixed
  ([#738](https://github.com/odpi/egeria-workspaces/pull/738)).
- **Analytic functions are found by registered name** ([#741](https://github.com/odpi/egeria-workspaces/pull/741),
  [#742](https://github.com/odpi/egeria-workspaces/pull/742), [#743](https://github.com/odpi/egeria-workspaces/pull/743)).

## Early November: relationship purposes, resizable panes, and a more accurate Overview

- **Relationships grouped by Egeria's relationship purpose** into six families in the Type Explorer, detail
  panels, Data Mesh and The Catalog; the Type Explorer shows inherited relationships and classifications
  ([#752](https://github.com/odpi/egeria-workspaces/pull/752), [#753](https://github.com/odpi/egeria-workspaces/pull/753),
  [#756](https://github.com/odpi/egeria-workspaces/pull/756), [#774](https://github.com/odpi/egeria-workspaces/pull/774),
  [#775](https://github.com/odpi/egeria-workspaces/pull/775)).
- **Every column, pane and split can be resized**, remembered per page ([#754](https://github.com/odpi/egeria-workspaces/pull/754)).
- **Lineage Explorer** hop limit and cut markers ([#749](https://github.com/odpi/egeria-workspaces/pull/749));
  Mermaid diagrams get an Expand viewer ([#781](https://github.com/odpi/egeria-workspaces/pull/781)).
- **The Overview only shows numbers it has actually measured.** Counts cover the whole repository, slow sections
  are measured in the background, and a card says "not measured" rather than showing a guess ([#783](https://github.com/odpi/egeria-workspaces/pull/783),
  [#785](https://github.com/odpi/egeria-workspaces/pull/785), [#788](https://github.com/odpi/egeria-workspaces/pull/788),
  [#790](https://github.com/odpi/egeria-workspaces/pull/790), [#793](https://github.com/odpi/egeria-workspaces/pull/793),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- A **Chief Data Officer dashboard** for Jules Keeper ([#780](https://github.com/odpi/egeria-workspaces/pull/780)).
- **Jupyter no longer trusts the emSign ECC G3 root** ([#776](https://github.com/odpi/egeria-workspaces/pull/776)).

## November 8 to 16: dashboards and report specs held in Egeria

- **Report specs show what they declare**, whether they can run, and if not, why not
  ([#809](https://github.com/odpi/egeria-workspaces/pull/809)); the Portal supplies a spec's inputs by role
  ([#806](https://github.com/odpi/egeria-workspaces/pull/806)).
- **Credentials are sent only to allow-listed platforms** ([#819](https://github.com/odpi/egeria-workspaces/pull/819)).
- **Dashboards are held in Egeria** behind a token-only API ([#818](https://github.com/odpi/egeria-workspaces/pull/818)),
  with result and sheet caches ([#814](https://github.com/odpi/egeria-workspaces/pull/814),
  [#815](https://github.com/odpi/egeria-workspaces/pull/815)); Report tiles pin collections by qualifiedName
  ([#824](https://github.com/odpi/egeria-workspaces/pull/824)); four ready-made sheets and repository trend tiles
  ([#826](https://github.com/odpi/egeria-workspaces/pull/826)).
- **Report specs are filed by the tool that uses them**, and Egeria Explorer shows a **Used by** row
  ([#821](https://github.com/odpi/egeria-workspaces/pull/821)).
- **Local Dashboards by folder**: a folder tree of Egeria-held sheets with Used by
  ([#829](https://github.com/odpi/egeria-workspaces/pull/829), [#830](https://github.com/odpi/egeria-workspaces/pull/830)).
- Collections grouped by type ([#816](https://github.com/odpi/egeria-workspaces/pull/816),
  [#817](https://github.com/odpi/egeria-workspaces/pull/817)); Insights saved queries refresh
  ([#823](https://github.com/odpi/egeria-workspaces/pull/823)).
- **Tutorials and worked examples** for saved queries, analytic functions, report specs and local dashboards
  ([#825](https://github.com/odpi/egeria-workspaces/pull/825)).
- **Classifications grouped by Egeria's classification purpose** (six purposes) in the Type Explorer, detail panels,
  Data Mesh and The Catalog; the `/api/types` routes no longer take a `user_id` parameter ([#831](https://github.com/odpi/egeria-workspaces/pull/831)).
- **Results tell you when something was left out**: pyegeria's notes, such as "more may exist", now appear under every result
  ([#852](https://github.com/odpi/egeria-workspaces/pull/852)); long tables are capped at whole rows and say the placement's real scope ([#848](https://github.com/odpi/egeria-workspaces/pull/848)); large tables
  scroll inside their tile with a sticky header ([#833](https://github.com/odpi/egeria-workspaces/pull/833)); `<br>` in a table cell is a line break ([#846](https://github.com/odpi/egeria-workspaces/pull/846)).
- **One renderer for pyegeria's structured TABLE** (`egeria-table.js`), used by Local Dashboards and Report Specs
  ([#855](https://github.com/odpi/egeria-workspaces/pull/855), [#856](https://github.com/odpi/egeria-workspaces/pull/856)).
- **DCAT support** in the quickstart and freshstart configurations, and an OpenLineage log store notebook
  ([#849](https://github.com/odpi/egeria-workspaces/pull/849), [#847](https://github.com/odpi/egeria-workspaces/pull/847)).
- **`egeria-upgrade-reset`**, a host CLI that plans and runs an Egeria upgrade or reset step by step, with a
  shared-infrastructure health check and a read-only "last reset" panel in Portal Admin ([#851](https://github.com/odpi/egeria-workspaces/pull/851), [#854](https://github.com/odpi/egeria-workspaces/pull/854),
  [#857](https://github.com/odpi/egeria-workspaces/pull/857)); after a reset, the sample content that used to be loaded by hand is now restored automatically ([#850](https://github.com/odpi/egeria-workspaces/pull/850)).
- **Egeria Advisor** (6.3 Tech Preview) gets its own service account, `egeriaadvisornpa` ([#828](https://github.com/odpi/egeria-workspaces/pull/828)).
- **Data Initialization shows each batch's status**, and only one run of a batch can be in progress at a time. Three
  Coco notebooks can now be run again safely, and new portal docs cover techniques and best practices for them
  ([#883](https://github.com/odpi/egeria-workspaces/pull/883)).
- **Statements of applicability**: a Coco sample for ISO/IEC 27001 ([#881](https://github.com/odpi/egeria-workspaces/pull/881)).
<!-- At the cut: the 6.3 bundle (RK-22 no hard-coded Portal folder GUID, Rocky's five-status branches, floor 6.3.0) and #885/#886 once merged; #882 if merged. -->

## Platform, infrastructure and dependencies

- **Platform**: the quickstart is pinned to the released Egeria 6.3 image, `odpi/egeria-platform:6.3` (#885).
  During the release cycle, quickstart and freshstart followed the Egeria 6.3-SNAPSHOT builds
  ([#647](https://github.com/odpi/egeria-workspaces/pull/647), [#748](https://github.com/odpi/egeria-workspaces/pull/748),
  [#798](https://github.com/odpi/egeria-workspaces/pull/798), [#800](https://github.com/odpi/egeria-workspaces/pull/800),
  [#805](https://github.com/odpi/egeria-workspaces/pull/805), [#808](https://github.com/odpi/egeria-workspaces/pull/808),
  [#810](https://github.com/odpi/egeria-workspaces/pull/810), [#827](https://github.com/odpi/egeria-workspaces/pull/827)).
- **pyegeria**: the image floors rose step by step from 6.2.7 to 6.2.24, and the images run newer releases
  (see PRs [#667](https://github.com/odpi/egeria-workspaces/pull/667) to [#802](https://github.com/odpi/egeria-workspaces/pull/802)).
  Freshstart is capped below 6.2.27 ([#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- **Shared infrastructure**: autoheal started, Postgres tuning and `pg_stat_statements` ([#686](https://github.com/odpi/egeria-workspaces/pull/686),
  [#804](https://github.com/odpi/egeria-workspaces/pull/804)); Kafka log size cap
  ([#820](https://github.com/odpi/egeria-workspaces/pull/820)); Marquez restarts after a reboot ([#857](https://github.com/odpi/egeria-workspaces/pull/857)); heap dump on out-of-memory
  ([#773](https://github.com/odpi/egeria-workspaces/pull/773)); Pasteur added to the nanny daemons
  ([#822](https://github.com/odpi/egeria-workspaces/pull/822)).
- **Dependencies**: Dependabot and consolidated bumps (dagster, playwright, Airflow, openlineage, confluent-kafka,
  mcp, schemathesis, pytest, Python base images, Prefect, certbot, docker) and the OpenSSF Scorecard workflow, which
  now runs.

Thank you to everyone who contributed: Dan Wolfson (313 commits), Mandy Chessell (23) and dependabot (41).

---

## Upgrade notes

- **Ports bind to `127.0.0.1`.** Add `--lan` to `quick-start-local` / `fresh-start-local` to reach the stack by
  machine name or from other machines.
- **Bearer tokens last two hours** ([#651](https://github.com/odpi/egeria-workspaces/pull/651)).
- **Report specs held in Egeria are read from the Portal's consumer folder.** The quickstart's default
  `PYEGERIA_REPORT_SPEC_FOLDERS` is now `ReportSpecFolder::Consumer::Portal`, under the root collection
  `RootCollection::ReportSpecs`; the old folder `ReportSpecFolder::EgeriaPortal` is no longer read. On each
  Egeria that a quickstart Portal reads, run
  `compose-configs/egeria-quickstart/PyegeriaWebHandler/egeria-held-specs/REPORT_SPEC_CONSUMER_FOLDERS.dr-egeria.md`
  once with Dr.Egeria (run `--validate` first). Until it has run, the Portal uses its local copies of its two
  specs, and the "Used by" row says "not read". To keep the old folder, set
  `PYEGERIA_REPORT_SPEC_FOLDERS=ReportSpecFolder::EgeriaPortal`.
- **Dashboard sheets held in Egeria** need the dashboard folder seeds (see PR
  [#829](https://github.com/odpi/egeria-workspaces/pull/829)). <!-- TODO: confirm the exact step for an existing Egeria. -->
- **Dashboard placements**: `emphasis` is renamed `presentationStyle`, and MeasurementSpecification references
  become relationships ([#796](https://github.com/odpi/egeria-workspaces/pull/796),
  [#795](https://github.com/odpi/egeria-workspaces/pull/795)).
- **Upgrading or resetting the quickstart Egeria**: use `compose-configs/egeria-quickstart/bin/egeria-upgrade-reset`
  (`plan` first, then `apply`); see *Upgrading or resetting the quickstart Egeria* ([#851](https://github.com/odpi/egeria-workspaces/pull/851)).
- **Rendered report text changed with pyegeria 6.2.37** (LIST cells, "more may exist" notes). Anything that parses
  the Portal's rendered tables should be re-checked; see the *Report Specs* tutorial, Part C ([#853](https://github.com/odpi/egeria-workspaces/pull/853)).
- **Postgres templates take a secrets store** ([#679](https://github.com/odpi/egeria-workspaces/pull/679)).
- **Egeria Advisor runs as `egeriaadvisornpa`** in quickstart ([#828](https://github.com/odpi/egeria-workspaces/pull/828)).
- **The quickstart needs pyegeria 6.2.42 or later** (6.3.0 recommended), and runs the released Egeria 6.3 image (#885). Freshstart
  still needs pyegeria `>=6.2.21,<6.2.27`.
- **`egeria-upgrade-reset plan --latest` is now `--stable`** and picks the newest released Egeria rather than the
  next release's development build. `--latest` still works (#886).

<!-- [IF #887 MERGES] then: switch every "6.2.42 or later; we recommend 6.3.0" to "pyegeria 6.3.0 or later (#887)", and add:
- **The Trellis database password no longer has a default.** Set `PGVECTOR_PASSWORD` in `compose-configs/shared-infra/.env`;
  `gen-env.sh` generates one for a new install. On an older install whose `egeria_advisor` role still uses the well-known
  password, change it first (see the shared-infra README, "Setting or changing the egeria_advisor password") (#887).
- **The first start after upgrading restarts the shared Postgres once** (see PR #887). -->

## Where the detail lives

The full list of changes, with links to each pull request, is in the `[6.3]` section of
[CHANGELOG.md](CHANGELOG.md). Work that is still open is in `BACKLOG.md`, and finished work is in
`BACKLOG-ARCHIVE.md`.
