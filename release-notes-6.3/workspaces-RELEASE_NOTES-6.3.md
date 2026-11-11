<!-- DRAFT: new top section for odpi/egeria-workspaces RELEASE_NOTES.md.
     At release: put this above "# Egeria Workspaces 6.2", demote 6.2's H1 if the file should hold several
     releases, and REMOVE the 6.2 file's "## Since 6.2 (unreleased, on main)" section (folded in below).
     Move 6.2's "Report specs held in Egeria are read from the Portal's consumer folder" upgrade note here
     (it describes 6.3 behaviour). Stats are from 903e8eeb (#619, 2026-10-09) to 48c94577 (#830, 2026-11-11);
     refresh them at the cut. TODO: release date, and whether a v6.2 tag gets created retroactively
     (no v6.2 tag exists; the compare link below assumes one). -->

# Egeria Workspaces 6.3

Five weeks, 195 merged changes, and dashboards and report specs that now live in Egeria.

Since the 6.2 release on October 9, `egeria-workspaces` has been about two things: keeping the reports and
dashboards people rely on in Egeria, where they are governed like any other metadata, and making every number
the Portal shows say what it actually measured. Around that, the demo stack was locked down by default, the
Portal gained a Resource Browser, relationships are grouped by purpose, and every width can be dragged. It
tracks the **Egeria 6.3** builds and **pyegeria 6.2.36**. **This is the 6.3 release.**

**6.3** &middot; **346** commits &middot; **195** merged PRs &middot; **75** feature commits &middot; **113** fix commits &middot; **5** weeks

## Try it

- **Live demo, no install**: **[egeria.pdr-associates.com](https://egeria.pdr-associates.com)**. Register
  free, pick a Coco Pharmaceuticals persona, explore in your browser. Open **Local Dashboards** to see sheets
  held in Egeria, by folder.
- **Run it yourself**: [Getting started](https://github.com/odpi/egeria-workspaces#getting-started)
  (Quickstart or Freshstart, local via Docker/Podman). Add `--lan` to reach the stack from other machines.
- **Learn by doing**: the new [Portal tutorials](portal-docs/tutorials/overview.md) on saved queries, analytic
  functions, report specs and local dashboards, with [worked examples](portal-docs/tutorials/worked-examples.md).

---

## Mid Oct: Resource Browser, and a demo that is locked down by default

- **Resource Browser** ([#620](https://github.com/odpi/egeria-workspaces/pull/620),
  [#621](https://github.com/odpi/egeria-workspaces/pull/621), [#622](https://github.com/odpi/egeria-workspaces/pull/622),
  [#625](https://github.com/odpi/egeria-workspaces/pull/625)): a page per resource with what it contains, its
  meaning and notes on its parts; search, home and browse; work lists and team sharing. Resource Explorer's
  **Curation Coverage** appears as a Dashboard Sheet tile ([#628](https://github.com/odpi/egeria-workspaces/pull/628)).
- **Public demo hardening** after the Obsidian compromise ([#640](https://github.com/odpi/egeria-workspaces/pull/640),
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

## Late Oct: lineage from Airflow, Coco content, and closing credential gaps

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

## Early Nov: relationship purposes, resizable widths, honest Overview

- **Relationships grouped by Egeria's relationship purpose** into six families in the Type Explorer, detail
  panels, Data Mesh and The Catalog; the Type Explorer shows inherited relationships and classifications
  ([#752](https://github.com/odpi/egeria-workspaces/pull/752), [#753](https://github.com/odpi/egeria-workspaces/pull/753),
  [#756](https://github.com/odpi/egeria-workspaces/pull/756), [#774](https://github.com/odpi/egeria-workspaces/pull/774),
  [#775](https://github.com/odpi/egeria-workspaces/pull/775)).
- **Every column, pane and split can be resized**, remembered per page ([#754](https://github.com/odpi/egeria-workspaces/pull/754)).
- **Lineage Explorer** hop limit and cut markers ([#749](https://github.com/odpi/egeria-workspaces/pull/749));
  Mermaid diagrams get an Expand viewer ([#781](https://github.com/odpi/egeria-workspaces/pull/781)).
- **The Overview shows only what it measured**: whole-repository counts, background measurement of slow sections,
  `asset_composition`, and "not measured" cards ([#783](https://github.com/odpi/egeria-workspaces/pull/783),
  [#785](https://github.com/odpi/egeria-workspaces/pull/785), [#788](https://github.com/odpi/egeria-workspaces/pull/788),
  [#790](https://github.com/odpi/egeria-workspaces/pull/790), [#793](https://github.com/odpi/egeria-workspaces/pull/793),
  [#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- A **Chief Data Officer dashboard** for Jules Keeper ([#780](https://github.com/odpi/egeria-workspaces/pull/780)).
- **Jupyter no longer trusts the emSign ECC G3 root** ([#776](https://github.com/odpi/egeria-workspaces/pull/776)).

## Nov 8–11: dashboards and report specs held in Egeria

- **Report specs show what they declare**, whether they can run, and why not
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
- **Egeria Advisor** gets its own service account, `egeriaadvisornpa` ([#828](https://github.com/odpi/egeria-workspaces/pull/828)).

## Underneath all of it

- **Platform**: quickstart and freshstart moved to Egeria 6.3-SNAPSHOT; the quickstart pin tracks the Pasteur build
  ([#647](https://github.com/odpi/egeria-workspaces/pull/647), [#748](https://github.com/odpi/egeria-workspaces/pull/748),
  [#798](https://github.com/odpi/egeria-workspaces/pull/798), [#800](https://github.com/odpi/egeria-workspaces/pull/800),
  [#805](https://github.com/odpi/egeria-workspaces/pull/805), [#808](https://github.com/odpi/egeria-workspaces/pull/808),
  [#810](https://github.com/odpi/egeria-workspaces/pull/810), [#827](https://github.com/odpi/egeria-workspaces/pull/827)).
  <!-- TODO: if Egeria 6.3 is released before the cut, re-pin to the 6.3 image, as 6.2 did. -->
- **pyegeria**: the image floors rose step by step from 6.2.7 to 6.2.24, and the images run newer releases
  (see PRs [#667](https://github.com/odpi/egeria-workspaces/pull/667) to [#802](https://github.com/odpi/egeria-workspaces/pull/802)).
  Freshstart is capped below 6.2.27 ([#807](https://github.com/odpi/egeria-workspaces/pull/807)).
- **Shared infrastructure**: autoheal started, Postgres tuning and `pg_stat_statements` ([#686](https://github.com/odpi/egeria-workspaces/pull/686),
  [#804](https://github.com/odpi/egeria-workspaces/pull/804)); Kafka log size cap
  ([#820](https://github.com/odpi/egeria-workspaces/pull/820)); heap dump on out-of-memory
  ([#773](https://github.com/odpi/egeria-workspaces/pull/773)); Pasteur added to the nanny daemons
  ([#822](https://github.com/odpi/egeria-workspaces/pull/822)).
- **Dependencies**: Dependabot and consolidated bumps (dagster, playwright, Airflow, openlineage, confluent-kafka,
  mcp, schemathesis, pytest, Python base images, Prefect, certbot, docker) and the OpenSSF Scorecard workflow, which
  now runs.

**Commits by author:** 292 — Dan Wolfson &middot; 33 — dependabot[bot] &middot; 21 — Mandy Chessell

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
- **Postgres templates take a secrets store** ([#679](https://github.com/odpi/egeria-workspaces/pull/679)).
- **Egeria Advisor runs as `egeriaadvisornpa`** in quickstart ([#828](https://github.com/odpi/egeria-workspaces/pull/828)).
- **Freshstart** needs pyegeria `>=6.2.21,<6.2.27`; the quickstart Portal needs a recent 6.2.x (see PR).
  <!-- TODO: state the quickstart floor at the cut (currently runs 6.2.36). -->

## Where the detail lives

The full list with PR links is in the `[6.3]` section of [CHANGELOG.md](CHANGELOG.md). Anything still open is in
`BACKLOG.md`; everything closed is in `BACKLOG-ARCHIVE.md`.

*egeria-workspaces 6.3 &middot; 6.2 (903e8eeb) → 6.3 &middot; compiled from git history*
