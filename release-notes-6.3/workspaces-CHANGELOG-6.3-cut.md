# Draft: CHANGELOG.md `[Unreleased]` → `[6.3]` cut (odpi/egeria-workspaces)

The current `[Unreleased]` section was written as items landed and stops around the relationship-purpose work
(early November). The cut is:

1. Rename the heading and open a fresh `[Unreleased]` above it:

   ```markdown
   ## [Unreleased]

   ## [6.3] - 2026-11-17

   This release goes with Egeria 6.3 and needs pyegeria 6.3.0 or later. [RELEASE_NOTES.md](RELEASE_NOTES.md) summarizes the main changes.
   ```

2. Keep every existing `[Unreleased]` entry, under the same Added / Changed / Fixed / Removed headings.
3. Add the entries below, which are not in `[Unreleased]` yet. Each heading says which section it goes in.
   Add a `### Security` heading for the security entries.
4. At the bottom, next to the existing `[6.2]` link, add:

   ```markdown
   [Unreleased]: https://github.com/odpi/egeria-workspaces/compare/v6.3...HEAD
   [6.3]: https://github.com/odpi/egeria-workspaces/compare/v6.2...v6.3
   ```

   `v6.2` is tagged at `903e8eeb` (#619), as the owner agreed on 2026-11-11. Tag `v6.3` at the release commit, on the
   release date, Tuesday 2026-11-17, alongside Egeria 6.3 (owner, 2026-11-16).

5. Remove the "Since 6.2 (unreleased, on `main`)" section from RELEASE_NOTES.md, since the new 6.3 section covers it.

---

### Added (append)

- **Coco systems feed Egeria, and Egeria feeds an operational data store** ([#870](https://github.com/odpi/egeria-workspaces/pull/870)).
  Egeria subscribes to the Coco products for people, roles, user identities, departments and locations, and the new
  Airflow DAG `coco_subscriptions_egeria` loads them into Egeria. A new `egeria_ods` database in the shared PostgreSQL,
  with a `provisioner` role, is set up to receive Egeria's own digital products, one table per product; tables arrive
  once Egeria's daily refresh subscriptions run on a schedule. `ensure-shared-infra.sh` runs `init_egeria_ods.sql` on
  every start, creating only what is missing. The Open Lineage Cataloguer's account now defines `publishZones` (empty),
  because from Egeria 6.3 publishing fails for an account that doesn't define it.
- **Dashboards held in Egeria.** Dashboard sheets and their tiles can be held in Egeria as Egeria 6.3 Dashboard
  elements with an owner, behind a token-only dashboards API ([#818](https://github.com/odpi/egeria-workspaces/pull/818)).
  Local Dashboards shows a folder tree of Egeria-held sheets with a Used by row
  ([#829](https://github.com/odpi/egeria-workspaces/pull/829), [#830](https://github.com/odpi/egeria-workspaces/pull/830)).
  Report tiles pin a collection by qualifiedName ([#824](https://github.com/odpi/egeria-workspaces/pull/824)).
  Server-side result and sheet caches keep placements quick
  ([#814](https://github.com/odpi/egeria-workspaces/pull/814), [#815](https://github.com/odpi/egeria-workspaces/pull/815)).
- **Four ready-made dashboard sheets and repository trend tiles** in the demo ([#826](https://github.com/odpi/egeria-workspaces/pull/826)).
- **Report spec declarations, resolution and refusals in the Portal**: each spec shows what it declares, whether it
  can run and why not ([#809](https://github.com/odpi/egeria-workspaces/pull/809)); the Portal supplies a spec's
  inputs by role ([#806](https://github.com/odpi/egeria-workspaces/pull/806)).
- **Resource Browser** phases 1 to 3 and the contents view: a page per resource, search, home, browse, work lists and
  team sharing ([#620](https://github.com/odpi/egeria-workspaces/pull/620), [#621](https://github.com/odpi/egeria-workspaces/pull/621),
  [#622](https://github.com/odpi/egeria-workspaces/pull/622), [#625](https://github.com/odpi/egeria-workspaces/pull/625)).
  **Curation Coverage** tile ([#628](https://github.com/odpi/egeria-workspaces/pull/628)).
- **Overview**: Trellis perspectives, `asset_composition`, background measurement of slow sections
  ([#788](https://github.com/odpi/egeria-workspaces/pull/788), [#793](https://github.com/odpi/egeria-workspaces/pull/793),
  [#790](https://github.com/odpi/egeria-workspaces/pull/790)).
- **Lineage Explorer** hop limit and cut markers ([#749](https://github.com/odpi/egeria-workspaces/pull/749)).
- **Resource Locator**: search on columns, attributes and data fields; several kinds at once; hover help on terms;
  set, change and clear Data Scope; create and edit Data Lenses that govern work lists ([#889](https://github.com/odpi/egeria-workspaces/pull/889)).
- **The Overview marks unconfirmed figures**: "at least N" or "N found", with the reason, when paging can't confirm
  a count read to the end, in the counts, viewer totals and the Ownership and Semantic Grounding tiles
  ([#890](https://github.com/odpi/egeria-workspaces/pull/890)).
- **Mermaid Expand viewer** ([#781](https://github.com/odpi/egeria-workspaces/pull/781)).
- **Filter and sort** on long relationship and property lists, and on schema, column and attribute-index tables
  ([#656](https://github.com/odpi/egeria-workspaces/pull/656), [#657](https://github.com/odpi/egeria-workspaces/pull/657));
  **View buttons** on schema rows and related elements ([#709](https://github.com/odpi/egeria-workspaces/pull/709)).
- **Collections grouped by type** ([#816](https://github.com/odpi/egeria-workspaces/pull/816), [#817](https://github.com/odpi/egeria-workspaces/pull/817)).
- **Data initialization runs notebooks** and scans roots for manifests ([#662](https://github.com/odpi/egeria-workspaces/pull/662)),
  with notebook docs and Data Hub notebooks ([#664](https://github.com/odpi/egeria-workspaces/pull/664),
  [#685](https://github.com/odpi/egeria-workspaces/pull/685)); usage workload batch ([#684](https://github.com/odpi/egeria-workspaces/pull/684)).
- **Workbenches isolated behind an egress allow-list** ([#733](https://github.com/odpi/egeria-workspaces/pull/733));
  evict a stuck workbench ([#739](https://github.com/odpi/egeria-workspaces/pull/739)).
- **Egeria Advisor service account** `egeriaadvisornpa` ([#828](https://github.com/odpi/egeria-workspaces/pull/828));
  Phoenix compose ([#645](https://github.com/odpi/egeria-workspaces/pull/645)); optional TestGen runtime
  ([#663](https://github.com/odpi/egeria-workspaces/pull/663)); Governance Engine view service
  ([#639](https://github.com/odpi/egeria-workspaces/pull/639)); Pepys (see PR [#636](https://github.com/odpi/egeria-workspaces/pull/636));
  Pasteur in the nanny daemons ([#822](https://github.com/odpi/egeria-workspaces/pull/822)).
- **Coco content**: Chief Data Officer dashboard for Jules Keeper ([#780](https://github.com/odpi/egeria-workspaces/pull/780)),
  Airflow DAGs ([#653](https://github.com/odpi/egeria-workspaces/pull/653)), system data layer
  ([#660](https://github.com/odpi/egeria-workspaces/pull/660)).
- **Dr.Egeria templates** for report specs and dashboards ([#803](https://github.com/odpi/egeria-workspaces/pull/803)).
- **Heap dump** when the platform runs out of memory ([#773](https://github.com/odpi/egeria-workspaces/pull/773));
  `pg_stat_statements` on the shared Postgres ([#804](https://github.com/odpi/egeria-workspaces/pull/804)).

- **DCAT support**: DCAT configuration for the quickstart and freshstart metadata stores and integration daemons,
  with loading-bay `dcat/` folders ([#849](https://github.com/odpi/egeria-workspaces/pull/849)); an OpenLineage log store notebook, and Pasteur in the nanny daemons
  ([#847](https://github.com/odpi/egeria-workspaces/pull/847)).
- **One renderer for pyegeria's structured TABLE** (`egeria-table.js`); Local Dashboards and Report Specs draw TABLE
  results from the structured shape ([#855](https://github.com/odpi/egeria-workspaces/pull/855), [#856](https://github.com/odpi/egeria-workspaces/pull/856)).
- **Data Initialization batch status**: each batch shows its status, one run per batch at a time; best-practice docs
  for the Data Initialization notebooks ([#883](https://github.com/odpi/egeria-workspaces/pull/883)).
- **Statements of Applicability view** in Egeria Explorer: an implementation summary and a sortable, filterable table
  of controls ([#882](https://github.com/odpi/egeria-workspaces/pull/882)).
- **Coco sample statement of applicability** for ISO/IEC 27001 ([#881](https://github.com/odpi/egeria-workspaces/pull/881)).
- **Dr.Egeria templates for Egeria 6.3**: Limit Result by Status lists the five element statuses, lifecycle filters
  are added, deployment status uses `REJECTED`, and activity status gains `FOR_INFO`. The templates match pyegeria
  6.3.0's ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **A Dr.Egeria best-practices doc** with the same status values ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **`init_trellis.sh`** creates the Trellis role and database from `PGVECTOR_PASSWORD`, and `gen-env.sh` generates
  that password for a brand-new install. The shared-infra README covers creating the role on an existing volume and
  setting or changing its password (TR-27, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The 16 MetadataExpert Dr.Egeria templates** (type and enum definitions, instances, classify, link and publish,
  Update Relationship, Count Metadata Elements), the same as pyegeria 6.3.0's ([#888](https://github.com/odpi/egeria-workspaces/pull/888)).

### Changed (append)

- **Platform**: quickstart and freshstart on Egeria 6.3-SNAPSHOT; the quickstart pin tracks the Pasteur build
  ([#647](https://github.com/odpi/egeria-workspaces/pull/647), [#748](https://github.com/odpi/egeria-workspaces/pull/748),
  [#740](https://github.com/odpi/egeria-workspaces/pull/740), [#798](https://github.com/odpi/egeria-workspaces/pull/798),
  [#800](https://github.com/odpi/egeria-workspaces/pull/800), [#805](https://github.com/odpi/egeria-workspaces/pull/805),
  [#808](https://github.com/odpi/egeria-workspaces/pull/808), [#810](https://github.com/odpi/egeria-workspaces/pull/810),
  [#827](https://github.com/odpi/egeria-workspaces/pull/827)).
- **Bearer tokens last two hours** ([#651](https://github.com/odpi/egeria-workspaces/pull/651)).
- **Analytic functions and metric paths by registered name** ([#741](https://github.com/odpi/egeria-workspaces/pull/741),
  [#742](https://github.com/odpi/egeria-workspaces/pull/742), [#743](https://github.com/odpi/egeria-workspaces/pull/743),
  [#811](https://github.com/odpi/egeria-workspaces/pull/811)).
- **Dashboard placements**: `presentationStyle` replaces `emphasis`; MeasurementSpecification references become
  relationships (docs: [#796](https://github.com/odpi/egeria-workspaces/pull/796), [#795](https://github.com/odpi/egeria-workspaces/pull/795)).
- **Freshstart catches up with the quickstart**: shared helper modules and 13 handlers
  ([#891](https://github.com/odpi/egeria-workspaces/pull/891)), then the Overview, with pyegeria 6.3.0 or later
  replacing the earlier cap below 6.2.27 ([#892](https://github.com/odpi/egeria-workspaces/pull/892),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- **pyegeria image floors** raised step by step to 6.2.24 ([#667](https://github.com/odpi/egeria-workspaces/pull/667),
  [#680](https://github.com/odpi/egeria-workspaces/pull/680), [#688](https://github.com/odpi/egeria-workspaces/pull/688),
  [#695](https://github.com/odpi/egeria-workspaces/pull/695), [#707](https://github.com/odpi/egeria-workspaces/pull/707),
  [#712](https://github.com/odpi/egeria-workspaces/pull/712), [#731](https://github.com/odpi/egeria-workspaces/pull/731),
  [#736](https://github.com/odpi/egeria-workspaces/pull/736), [#751](https://github.com/odpi/egeria-workspaces/pull/751),
  [#772](https://github.com/odpi/egeria-workspaces/pull/772), [#789](https://github.com/odpi/egeria-workspaces/pull/789),
  [#802](https://github.com/odpi/egeria-workspaces/pull/802)).
- **Shared infrastructure**: autoheal started and Postgres checkpointing tuned ([#686](https://github.com/odpi/egeria-workspaces/pull/686));
  Airflow lineage to Egeria only ([#784](https://github.com/odpi/egeria-workspaces/pull/784)); Kafka's own server logs
  capped by size ([#820](https://github.com/odpi/egeria-workspaces/pull/820)).
- **Dependencies**: Dependabot and consolidated bumps ([#652](https://github.com/odpi/egeria-workspaces/pull/652),
  [#708](https://github.com/odpi/egeria-workspaces/pull/708), [#718](https://github.com/odpi/egeria-workspaces/pull/718),
  [#737](https://github.com/odpi/egeria-workspaces/pull/737), [#757](https://github.com/odpi/egeria-workspaces/pull/757)
  to [#771](https://github.com/odpi/egeria-workspaces/pull/771)); Actions bumps ([#542](https://github.com/odpi/egeria-workspaces/pull/542),
  [#543](https://github.com/odpi/egeria-workspaces/pull/543), [#596](https://github.com/odpi/egeria-workspaces/pull/596),
  [#764](https://github.com/odpi/egeria-workspaces/pull/764), [#765](https://github.com/odpi/egeria-workspaces/pull/765)).
- **pyegeria 6.3.0 is the quickstart's minimum**, in the four Dockerfiles and `requirements.txt` ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The Portal's report-spec consumer folder is found by its qualified name**, not a hard-coded GUID (RK-22, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).
- **The shared Postgres service gains a `PGVECTOR_PASSWORD` setting**, so the first start after upgrading recreates
  the `egeria-shared-postgres` container once. Data and existing passwords are kept ([#887](https://github.com/odpi/egeria-workspaces/pull/887)).

### Fixed (append)

- **The Overview shows only what it measured** ([#783](https://github.com/odpi/egeria-workspaces/pull/783),
  [#785](https://github.com/odpi/egeria-workspaces/pull/785), [#791](https://github.com/odpi/egeria-workspaces/pull/791),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)); the Overview no longer stops running
  `egeria-shared-ui.js` halfway ([#755](https://github.com/odpi/egeria-workspaces/pull/755)).
- **The Catalog**: every list pages to the end, Data Assets tree, list caches ([#659](https://github.com/odpi/egeria-workspaces/pull/659),
  [#658](https://github.com/odpi/egeria-workspaces/pull/658), [#661](https://github.com/odpi/egeria-workspaces/pull/661),
  [#666](https://github.com/odpi/egeria-workspaces/pull/666)).
- **Blank Data Mesh and Resource Locator pages; text contrast** ([#654](https://github.com/odpi/egeria-workspaces/pull/654),
  [#655](https://github.com/odpi/egeria-workspaces/pull/655)).
- **Type Explorer** fixes ([#777](https://github.com/odpi/egeria-workspaces/pull/777), [#750](https://github.com/odpi/egeria-workspaces/pull/750),
  [#745](https://github.com/odpi/egeria-workspaces/pull/745), [#746](https://github.com/odpi/egeria-workspaces/pull/746));
  solution components ([#716](https://github.com/odpi/egeria-workspaces/pull/716), [#717](https://github.com/odpi/egeria-workspaces/pull/717)).
- **Information supply chain graphs on Egeria 6.3**, and a 404 for a missing supply chain
  ([#710](https://github.com/odpi/egeria-workspaces/pull/710), [#648](https://github.com/odpi/egeria-workspaces/pull/648)).
- **Demo reset** ([#646](https://github.com/odpi/egeria-workspaces/pull/646), [#729](https://github.com/odpi/egeria-workspaces/pull/729));
  shared infra ([#624](https://github.com/odpi/egeria-workspaces/pull/624)); loading bay Bitol folder
  ([#681](https://github.com/odpi/egeria-workspaces/pull/681)); secrets refresh ([#638](https://github.com/odpi/egeria-workspaces/pull/638));
  empty limits ([#641](https://github.com/odpi/egeria-workspaces/pull/641)); compose build ([#626](https://github.com/odpi/egeria-workspaces/pull/626));
  the self-heal step now loads valid metadata values first ([#801](https://github.com/odpi/egeria-workspaces/pull/801)).
- **MCP SSE headers** ([#738](https://github.com/odpi/egeria-workspaces/pull/738)).
- **Three Coco Data Initialization notebooks** fit their cell limits and are safe to run again; the Local Dashboards
  Dr.Egeria inbox models its subscription as a Digital Subscription ([#883](https://github.com/odpi/egeria-workspaces/pull/883)).
- **Marquez restarts after a reboot**, and the infra check covers `airflow-marquez` ([#857](https://github.com/odpi/egeria-workspaces/pull/857)); the scheduled infra
  check writes one bounded log line per run ([#854](https://github.com/odpi/egeria-workspaces/pull/854)).
- **`gen-env.sh` quotes the Kafka directory paths**, so shared infrastructure starts from a checkout whose path contains
  a space ([#888](https://github.com/odpi/egeria-workspaces/pull/888)).

### Security (new heading)

- **No well-known password for the `provisioner` database user.** It comes from `PROVISIONER_PASSWORD` in
  `shared-infra/.env`, generated when missing; the first start rotates it with the runtime secrets and Airflow, and
  it is kept out of `pg_stat_statements`' query-text file (TR-28, [#889](https://github.com/odpi/egeria-workspaces/pull/889)).
- **Credentials are sent only to allow-listed Egeria platforms** ([#819](https://github.com/odpi/egeria-workspaces/pull/819)).
- **A signed-in user's request is never run as the service user** ([#715](https://github.com/odpi/egeria-workspaces/pull/715)).
- **Continued hardening of the Portal environment** ([#640](https://github.com/odpi/egeria-workspaces/pull/640),
  [#642](https://github.com/odpi/egeria-workspaces/pull/642), [#643](https://github.com/odpi/egeria-workspaces/pull/643)).
- **Ports bind to `127.0.0.1` by default** ([#644](https://github.com/odpi/egeria-workspaces/pull/644)); `--lan` opens them
  ([#687](https://github.com/odpi/egeria-workspaces/pull/687)).
- **Jupyter no longer trusts the emSign ECC G3 root** ([#776](https://github.com/odpi/egeria-workspaces/pull/776)).
- **No default `egeria_advisor` password**: `init_egeria.sql` no longer creates the role with a well-known password
  (TR-27, [#887](https://github.com/odpi/egeria-workspaces/pull/887)).
