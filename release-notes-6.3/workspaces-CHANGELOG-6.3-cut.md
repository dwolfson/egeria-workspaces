# Draft: CHANGELOG.md `[Unreleased]` → `[6.3]` cut (odpi/egeria-workspaces)

The current `[Unreleased]` section was written as items landed and stops around the relationship-purpose work
(early November). The cut is:

1. Rename the heading and open a fresh `[Unreleased]` above it:

   ```markdown
   ## [Unreleased]

   ## [6.3] - 2026-11-16

   Aligns with Egeria 6.3 and pyegeria 6.2.37 and later. See [RELEASE_NOTES.md](RELEASE_NOTES.md) for the narrative summary.
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
   release date (tentatively Monday 2026-11-16, alongside Egeria 6.3).

5. Remove the "Since 6.2 (unreleased, on `main`)" section from RELEASE_NOTES.md, since the new 6.3 section covers it.

---

### Added (append)

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
- **Freshstart pyegeria capped below 6.2.27** ([#807](https://github.com/odpi/egeria-workspaces/pull/807)); image
  floors raised step by step to 6.2.24 ([#667](https://github.com/odpi/egeria-workspaces/pull/667),
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
  heal primes valid metadata ([#801](https://github.com/odpi/egeria-workspaces/pull/801)).
- **MCP SSE headers** ([#738](https://github.com/odpi/egeria-workspaces/pull/738)).
- **Marquez restarts after a reboot**, and the infra check covers `airflow-marquez` ([#857](https://github.com/odpi/egeria-workspaces/pull/857)); the scheduled infra
  check writes one bounded log line per run ([#854](https://github.com/odpi/egeria-workspaces/pull/854)).

### Security (new heading)

- **Credentials are sent only to allow-listed Egeria platforms** ([#819](https://github.com/odpi/egeria-workspaces/pull/819)).
- **A signed-in user's request is never run as the service user** ([#715](https://github.com/odpi/egeria-workspaces/pull/715)).
- **Public demo hardening and Obsidian lock-down** ([#640](https://github.com/odpi/egeria-workspaces/pull/640),
  [#642](https://github.com/odpi/egeria-workspaces/pull/642), [#643](https://github.com/odpi/egeria-workspaces/pull/643)).
- **Ports bind to `127.0.0.1` by default** ([#644](https://github.com/odpi/egeria-workspaces/pull/644)); `--lan` opens them
  ([#687](https://github.com/odpi/egeria-workspaces/pull/687)). Move the existing `--lan` entry here or cross-reference it.
- **Jupyter no longer trusts the emSign ECC G3 root** ([#776](https://github.com/odpi/egeria-workspaces/pull/776)).
- **Obsidian plugin dependencies** ([#704](https://github.com/odpi/egeria-workspaces/pull/704)): already under Changed; move here.

### Not itemised

Docs-only PRs (design notes and Portal Docs reorganisation: #649, #683, #728, #778, #782, #786, #787, #792, #794,
#797, #799, #813), CI chores (#744, #747, #768, #779) and the "keep RELEASE_NOTES per release" note. Dependabot bumps after #830 (#834–#837, #839, #841–#843) go under the existing
Dependencies entry. Add any of them if the owner wants them listed.
