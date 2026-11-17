# Egeria Workspaces 6.3

Since the 6.2 release on October 9, our work on `egeria-workspaces` has focused on:

* Keeping up with the new features in Egeria, and making them easy to reach and to observe.
* Extending reports and dashboards into Egeria, while still letting users and teams create and manage
  their own local ones.
* Improving the accuracy and transparency of the measurements, metrics and KPIs we display.

This release goes with **Egeria 6.3** and needs **pyegeria 6.3.0 or later**, the release that matches Egeria 6.3. For the changes to the Egeria
platform itself, see the [Egeria 6.3 release notes](https://egeria-project.org/release-notes/latest/) and the
[November 2026 newsletter](https://egeria-project.org/release-notes/november-2026/).

In numbers: 499 commits and 253 merged pull requests between October 9 and November 17.

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

## November 8 to 17: dashboards and report specs held in Egeria

- **The Resource Locator searches more and explains itself.** Search finds columns, attributes and data fields, and
  can search several kinds at once. Hover over a term on the page to see what it means. You can set, change and clear
  a resource's Data Scope, and create and edit Data Lenses that govern work lists ([#889](https://github.com/odpi/egeria-workspaces/pull/889)).
- **Browse the Resource Locator by folder, search keyword or category**, and search glossary terms too. Filter Browse
  lists by a Data Lens, tick several results and add them to a work list at once, and follow a breadcrumb back to
  your list with its search and filters kept. A Data Scope of a year, month or day covers the whole of it
  ([#893](https://github.com/odpi/egeria-workspaces/pull/893)).
<!-- STAGED until #894 merges. Then change "with its search and filters kept" above to "with its search, filters,
  scroll and the rows you opened with Show more kept" and add [#894](https://github.com/odpi/egeria-workspaces/pull/894) to the line. -->
- **The Overview marks figures it could not confirm.** When paging can't confirm that a count read to the end, the
  figure says "at least N" or "N found", with the reason, instead of a bare number that might be wrong
  ([#890](https://github.com/odpi/egeria-workspaces/pull/890)).
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
- **Coco's own systems feed Egeria, and Egeria feeds a SQL store** ([#870](https://github.com/odpi/egeria-workspaces/pull/870)).
  Egeria subscribes to the Coco products that describe people, roles, user identities, departments and locations,
  and a new Airflow DAG, `coco_subscriptions_egeria`, loads the deliveries into Egeria. A new `egeria_ods` database in
  the shared PostgreSQL is set up to receive Egeria's own digital products, one table per product, so open metadata
  can be queried with SQL. Its tables arrive once Egeria's daily refresh subscriptions run on a schedule, which needs
  a companion Egeria change (see the PR).
- **Statements of applicability**: Egeria Explorer has a new Statements of Applicability view, with an implementation
  summary and a table of controls you can sort and filter ([#882](https://github.com/odpi/egeria-workspaces/pull/882)), and Coco has a sample for ISO/IEC 27001
  ([#881](https://github.com/odpi/egeria-workspaces/pull/881)).

## Platform, infrastructure and dependencies

- **Platform**: the quickstart is pinned to the released Egeria 6.3 image, `odpi/egeria-platform:6.3` (#885).
  During the release cycle, quickstart and freshstart followed the Egeria 6.3-SNAPSHOT builds
  ([#647](https://github.com/odpi/egeria-workspaces/pull/647), [#748](https://github.com/odpi/egeria-workspaces/pull/748),
  [#798](https://github.com/odpi/egeria-workspaces/pull/798), [#800](https://github.com/odpi/egeria-workspaces/pull/800),
  [#805](https://github.com/odpi/egeria-workspaces/pull/805), [#808](https://github.com/odpi/egeria-workspaces/pull/808),
  [#810](https://github.com/odpi/egeria-workspaces/pull/810), [#827](https://github.com/odpi/egeria-workspaces/pull/827)).
- **pyegeria**: the image floors rose step by step from 6.2.7 to 6.2.24, and the images run newer releases
  (see PRs [#667](https://github.com/odpi/egeria-workspaces/pull/667) to [#802](https://github.com/odpi/egeria-workspaces/pull/802)).
  Freshstart, briefly capped below 6.2.27 ([#807](https://github.com/odpi/egeria-workspaces/pull/807)), now needs
  pyegeria 6.3.0 or later too. Its Portal catches up with the quickstart's: shared helper modules and 11 handlers
  ([#891](https://github.com/odpi/egeria-workspaces/pull/891)), then the Overview, with "not measured" and the
  unconfirmed marks ([#892](https://github.com/odpi/egeria-workspaces/pull/892)).
- **Shared infrastructure**: autoheal started, Postgres tuning and `pg_stat_statements` ([#686](https://github.com/odpi/egeria-workspaces/pull/686),
  [#804](https://github.com/odpi/egeria-workspaces/pull/804)); Kafka log size cap
  ([#820](https://github.com/odpi/egeria-workspaces/pull/820)); Marquez restarts after a reboot ([#857](https://github.com/odpi/egeria-workspaces/pull/857)); heap dump on out-of-memory
  ([#773](https://github.com/odpi/egeria-workspaces/pull/773)); Pasteur added to the nanny daemons
  ([#822](https://github.com/odpi/egeria-workspaces/pull/822)).
- **Dependencies**: Dependabot and consolidated bumps (dagster, playwright, Airflow, openlineage, confluent-kafka,
  mcp, schemathesis, pytest, Python base images, Prefect, certbot, docker) and the OpenSSF Scorecard workflow, which
  now runs.

Thank you to everyone who contributed: Dan Wolfson (422 commits), Mandy Chessell (27) and dependabot (50).

---

## Upgrade notes

### Upgrading an existing install, in order

1. **Stop everything that uses the shared PostgreSQL**: the quickstart or freshstart stack, Airflow and Marquez, and
   the AI applications.
2. **Update your checkout** to this release.
3. **Set `PGVECTOR_PASSWORD`** in `compose-configs/shared-infra/.env`. The database used by the AI applications no
   longer has a default password. `gen-env.sh` generates one only when the data volume is new; on an existing
   install whose `egeria_advisor` role still has the old well-known password, change it first (see the shared-infra
   README, "Setting or changing the egeria_advisor password"), then put the new value in `.env`
   ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
4. **Start the shared infrastructure.** The first time, Docker recreates the `egeria-shared-postgres` container once,
   because its configuration gained the `PGVECTOR_PASSWORD` setting; your data is kept
   ([#887](https://github.com/odpi/egeria-workspaces/pull/887)). Other shared containers are recreated too if their
   images changed. Every start now also creates the `egeria_ods` database and the `provisioner` role if they are
   missing ([#870](https://github.com/odpi/egeria-workspaces/pull/870)).
5. **Start with `--with-airflow-marquez`**, so the Airflow containers are recreated and get the new `egeria`
   connection. Until they are, the new DAG `coco_subscriptions_egeria`, which starts unpaused, fails on every run
   because that connection is missing. If you don't want it yet, pause it in Airflow
   ([#870](https://github.com/odpi/egeria-workspaces/pull/870)).
   The same start gives the `provisioner` database user its own password, kept in `PROVISIONER_PASSWORD` in
   `compose-configs/shared-infra/.env` (generated if missing, on existing installs too), and updates the runtime
   secrets and Airflow's connection to match, which is why Airflow must be restarted in the same run
   ([#889](https://github.com/odpi/egeria-workspaces/pull/889)).
<!-- STAGED until #894 merges. Then append to step 5:
   The `provisioner` role is shared, and the new password reaches only the stack you start. If one host runs both
   the quickstart and a freshstart, run the other stack's start script too, or its provisioning connectors can't
   sign in ([#894](https://github.com/odpi/egeria-workspaces/pull/894)).
-->
6. **Rebuild the images.** The quickstart needs pyegeria 6.3.0 or later
   ([#887](https://github.com/odpi/egeria-workspaces/pull/887)) and runs the released Egeria 6.3 image
   ([#885](https://github.com/odpi/egeria-workspaces/pull/885)). Freshstart now needs pyegeria 6.3.0 or later too
   ([#892](https://github.com/odpi/egeria-workspaces/pull/892)).
<!-- STAGED until #894 merges. Then insert as step 7 and renumber the next step to 8:
7. **If you run Resource Explorer and Egeria Advisor (Trellis), set `TRELLIS_DB_CREDENTIAL_KEY`.** It is now
   required in `compose-configs/optional-associated-runtimes/trellis/.env`, and the Prefect Resource Explorer worker
   needs the same value in `.env.re-worker`; without it, compose won't start the Resource Explorer containers (a
   Resource Explorer you run on the host falls back to a host-name key and warns). Generate it once (for example
   `openssl rand -hex 32`) and keep it stable. Before this, the key that encrypts stored database passwords came from
   the container's host name, so each recreate made them unreadable: re-enter each stored database password once.
   If an older `.env` sets `RE_DB_CREDENTIAL_KEY`, that one takes precedence, so leave it unset or give it the same
   value ([#894](https://github.com/odpi/egeria-workspaces/pull/894)).
-->
7. **To upgrade or reset the quickstart's Egeria itself**, use `compose-configs/egeria-quickstart/bin/egeria-upgrade-reset`
   (`plan` first, then `apply`); see *Upgrading or resetting the quickstart Egeria*
   ([#851](https://github.com/odpi/egeria-workspaces/pull/851)). `plan --stable` picks the newest released Egeria;
   `--latest` is now another name for it ([#886](https://github.com/odpi/egeria-workspaces/pull/886)).

### Other changes to know about

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
- **Dashboard sheets held in Egeria are listed from the dashboard folders.** On an existing Egeria, run the
  **Dashboard Folders** batch and then **Useful Dashboards** from Data Initialization in Portal Admin; on a new
  install they run by default ([#829](https://github.com/odpi/egeria-workspaces/pull/829)).
- **Dashboard placements**: `emphasis` is renamed `presentationStyle`, and MeasurementSpecification references
  become relationships ([#796](https://github.com/odpi/egeria-workspaces/pull/796),
  [#795](https://github.com/odpi/egeria-workspaces/pull/795)).
- **Rendered report text changed with pyegeria 6.2.37** (LIST cells, "more may exist" notes). Anything that parses
  the Portal's rendered tables should be re-checked; see the *Report Specs* tutorial, Part C ([#853](https://github.com/odpi/egeria-workspaces/pull/853)).
- **Postgres templates take a secrets store** ([#679](https://github.com/odpi/egeria-workspaces/pull/679)).
- **Egeria Advisor runs as `egeriaadvisornpa`** in quickstart ([#828](https://github.com/odpi/egeria-workspaces/pull/828)).
- **Counts show what the signed-in user can see.** Elements anchored to Promise or Memento elements appear only with
  the Promise / Memento toggle on, and content in a governance zone appears only to users with access to that zone.
- **If you call pyegeria's `find_data_assets` yourself** (in notebooks or scripts), it returns only ACTIVE assets by
  default; pass `content_status_list=[]` to include assets with no content status. The Portal's lists already do.
- **`fresh-start-local` waits for the platform to report healthy**, and handles Podman the way `quick-start-local`
  does. Re-running a start script keeps the `provisioner` password; the shared-infra README says when a new one is
  made ([#893](https://github.com/odpi/egeria-workspaces/pull/893)).

## Where the detail lives

The full list of changes, with links to each pull request, is in the `[6.3]` section of
[CHANGELOG.md](CHANGELOG.md). Work that is still open is in `BACKLOG.md`, and finished work is in
`BACKLOG-ARCHIVE.md`.
