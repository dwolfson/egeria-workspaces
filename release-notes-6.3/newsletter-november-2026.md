<!-- DRAFT for egeria-docs: site/docs/release-notes/november-2026.md
     Status: draft 2026-11-11, from release-notes-6.3/RELEASE-NOTES-NEXT.md.
     Open points are marked TODO. Also add the page to site/mkdocs.yml (nav), as fb489c6b did for October.
     Screenshots: draft shots (800x500, laz, as erinoverview, 2026-11-13) are in release-notes-6.3/images/;
     each TODO-IMAGE says what to retake at full resolution.
     Owner decision 2026-11-11: this is OUR PIECE of the Egeria project's 6.3 release notes/newsletter, not the whole
     newsletter. The project supplies the opening, the core Egeria 6.3 platform sections, the link to the full 6.3
     release notes and upgrade notes. The opening paragraph, "Future plans" and "Connecting with the project" below are
     placeholders in October's wording, for the project to keep, replace or merge.
     Release: tentatively Monday 2026-11-16, alongside Egeria 6.3. Resource Explorer and Egeria Advisor are "6.3 Tech Preview". -->
<!-- SPDX-License-Identifier: CC-BY-4.0 -->
<!-- Copyright Contributors to the Egeria project. -->

# November 2026

Welcome to the Egeria community's November 2026 newsletter. Since our [last newsletter](https://egeria-project.org/release-notes/october-2026/) we have been working towards **Egeria 6.3**. This newsletter covers what has changed in Egeria Workspaces, Resource Explorer, Egeria Advisor and pyegeria over those five weeks.

<!-- PROJECT SECTIONS GO HERE: the core Egeria 6.3 platform "What's new" and the link to the full 6.3 release notes.
     Platform features our tools depend on, which the project's sections may want to mention: report specs,
     measurements and dashboards as Egeria elements; relationship purposes; boxed properties; information supply
     chain graphs; lineage hop limits; statements of applicability; the zone access rule. -->

In October we said that AI agents and applications are only as trustworthy as the context they work from. This release applies that idea to our own tools. A number on a dashboard now says what it counted, or says that it was not measured. The reports and dashboards people rely on are kept in Egeria, so they are governed like any other metadata. And Resource Explorer and Egeria Advisor, the early previews we showed in October, are now a Tech Preview.

<!-- TODO-IMAGE: Portal Local Dashboards, folder tree on the left, one of the "useful" sheets open
     (for example the repository trends sheet), signed in as a Coco persona. File: november-2026-local-dashboards.png
     DRAFT shot taken 2026-11-13 as erinoverview on laz at 800x500 (pane limit); retake at full resolution before publishing. Alternative: images/november-2026-local-dashboards-list.jpg (the sheet list with folders and Used by). -->
![The Catalog Health dashboard sheet, held in Egeria, showing AI-readiness counts, asset ownership, stale assets and asset composition](november-2026-local-dashboards.jpg)

## What's new

### Dashboards and report specs kept in Egeria

Until now, the Portal's dashboards and the report specs behind them were files on the server. With Egeria 6.3 they can be held in Egeria itself. Dashboard sheets and their tiles are Egeria elements with an owner, organised in folders, and the Portal's Local Dashboards page shows them by folder. Report specs are filed in a folder for each tool that uses them (the Portal, Egeria Advisor, Resource Explorer, pyegeria, My Egeria and Jupyter): putting a spec in a tool's folder publishes it to that tool. Egeria Explorer shows a "Used by" row for every spec.

Because they are Egeria elements, specs and dashboards get what every other piece of metadata gets: zones, ownership, history and search. A spec can also be restricted, so only the people allowed to see it can run it. Before a spec runs, the Portal shows what it declares, whether it can run, and, if it cannot, why. Egeria Advisor can read and author the same dashboards, so a dashboard built in one tool appears in the other.

The demo comes with four new ready-made sheets, including repository trend tiles.

Learn more about [Local Dashboards](https://github.com/odpi/egeria-workspaces/blob/main/portal-docs/tools/local-dashboards.md) and [report specs held in Egeria](https://github.com/odpi/egeria-workspaces/blob/main/portal-docs/tutorials/report-specs.md).

### Numbers that say what they measured

A count that was never taken is not zero, and a list that stopped at its limit is not a total. We went through the Egeria Overview, the dashboards and the report results and removed every place where "not measured" could show as 0, or a cap as a total. Totals now count the whole repository, slow sections are measured in the background, each count says which population it covers, and anything not measured says so. Resource Explorer follows the same rule: a database it has not surveyed is "not established", not empty. Report results now carry their own notes, such as "Showing the first 100; more may exist", and the Portal shows them under every result; long tables are cut only at whole rows, and they say how many rows they left out.

This matters most when an AI reads the numbers. An agent that sees "0 quality issues" when nothing was checked will report good news that isn't true.

Learn more about the [Egeria Overview](https://github.com/odpi/egeria-workspaces/blob/main/portal-docs/tools/egeria-overview.md).

### Relationships and classifications grouped by purpose

Egeria gives every relationship type a purpose. The Portal uses it to group relationships into six families: Composition, Governance & Description, Organization, Associations, Design & Deployment, and Operations. You see the same grouping in the Type Explorer, the detail panels, the Data Mesh view and The Catalog, so a busy element's relationships are much easier to read. The Type Explorer also now shows inherited relationships and classifications. Classifications are grouped the same way, by Egeria's six classification purposes: Governance, Governance Implementation, Category, Descriptive, Analytical and Management.

Across the Portal, every column, pane and split can be resized, and each page remembers your widths.

Learn more about [relationship purposes](https://github.com/odpi/egeria-workspaces/blob/main/portal-docs/tools/egeria-explorer.md#relationship-purposes).

<!-- TODO-IMAGE: a detail panel with relationships folded into purpose families. File: november-2026-relationship-purposes.png
     DRAFT shot taken 2026-11-13 as erinoverview on laz at 800x500 (pane limit); retake at full resolution before publishing. -->
![The Customer API in The Catalog, with its 15 relationships folded into Composition, Governance & Description, and Design & Deployment](november-2026-relationship-purposes.jpg)

### Tutorials and analytic functions

New tutorials take you through saved queries, writing and registering analytic functions, report specs and local dashboards, each with worked examples that show the input, the steps and the result. Analytic functions and report specs are now found by their registered name, so a function you register once can be used from Jupyter, the Portal and Egeria Advisor.

Learn more in the [Portal tutorials](https://github.com/odpi/egeria-workspaces/blob/main/portal-docs/tutorials/overview.md).

### Secure by default

The demo environment is now locked down by default. Published ports answer only on the local machine unless you ask for them to be opened (`--lan`). Workbenches can only reach an allow-list of outside hosts. Containers that become unhealthy restart themselves. The Portal only ever sends credentials to approved Egeria platforms. A signed-in user's request is never run under a service account: Resource Explorer acts as the signed-in caller on every request, and Egeria Advisor runs Dr.Egeria as the signed-in user. We also removed trust in the emSign ECC G3 root certificate after its key was compromised.

## Egeria Workspaces

Egeria Workspaces, our ready-to-run environment, now tracks the Egeria 6.3 builds. Along with Egeria-held dashboards and report specs, it adds:

- **Resource Browser and Resource Locator**: a page for each resource showing what it contains, what it means, and notes on its parts, with search, work lists and team sharing.
- **The Catalog**: a tab for each kind of infrastructure, View buttons on schema rows, lists that page to the end, and data assets shown as a tree of their types.
- **Lineage Explorer**: a hop limit, with markers where the graph was cut.
- **Data initialization runs notebooks** as well as Dr.Egeria files.
- **Airflow and Marquez start with the demo**, and Airflow's lineage flows into Egeria through OpenLineage.
- **Coco Pharmaceuticals content**: a Chief Data Officer dashboard, security support, sustainability reference data, and Airflow pipelines that bring the digital products to life.

<!-- TODO-IMAGE: Resource Browser page for one Coco resource. File: november-2026-resource-browser.png
     Owner 2026-11-16: Resource Locator updates are in progress; retake this shot (and any Locator shots in the blog 11 tour) only after they land on laz.
     Coordinator 2026-11-17 00:00:26Z: the Locator chain is LIVE on laz (L4 091bba00): search on columns and attributes, a multi-type filter,
     hover help on terms, Data Scope / Data Lens editing, refreshed docs. Branches claude/rl-* (to claude/rl-docs 428a0155) go to odpi in the
     next bundled PR; PR is odpi/egeria-workspaces#889 (open); entries staged in the workspaces notes. Show these features in the retake.
     DRAFT shot taken 2026-11-13 as erinoverview on laz at 800x500 (pane limit); retake at full resolution before publishing. -->
![The Resource Locator page for the Customer API: what it contains, its lineage, and its usage activity](november-2026-resource-browser.jpg)

You can [try the live demo](https://egeria.pdr-associates.com){target=blank} without installing anything (signing up takes a minute), or run [Egeria Workspaces](https://egeria-project.org/egeria-workspaces/) locally with Docker or Podman.

## Tech Preview: Resource Explorer and Egeria Advisor

In October we shared these two [Trellis](https://egeria-project.org/concepts/trellis/) applications as early previews. Thank you to everyone who tried them. Five weeks and more than 500 changes later, they are released together as the **6.3 Tech Preview**. They still run alongside Egeria Workspaces as an optional add-on, and both are available on the [live demo](https://egeria.pdr-associates.com){target=blank}: open them from their tiles on the Portal home page.

**Resource Explorer** surveys resources that are not yet in the catalog and helps you decide what to catalog. In this release:

- **It publishes to Egeria.** Curated results become Egeria elements, with a check that they arrived. What Resource Explorer creates is placed in the right zones, and private material is published only as its owner. If a publish fails, it says why in plain language.
- **Its surveys run through Egeria.** Surveys are registered as Egeria survey definitions that Egeria's engine host runs, and each step sends an OpenLineage event, so a survey has lineage like any other process.
- **It looks deeper.** For databases: table sizes, materialized views, activity, value profiles and quality checks, published to Egeria as quality annotations. For files: CSV, Parquet and Delta Lake. For open data: datasets from DOI, DataCite and DCAT-AP sources.
- **It answers better.** Questions about a resource search that resource's own documents first. Links between assets come with a stated level of confidence. Answers are formatted.
- **It has a new interface** with Dark, Light and Paper looks, cards and tiles, and a graph view.
- **It learns from you.** When you rate an answer you can say why. An administrator reviews the feedback and can trace a problem back to a gap in the documents. The document index can be rebuilt, swapped in and rolled back.
- **A six-part tutorial** takes you from signing in to analysis.

<!-- TODO-IMAGE: Resource Explorer Next UI, a database resource with cards and tiles. File: november-2026-resource-explorer.png
     DRAFT shot taken 2026-11-13 as erinoverview on laz at 800x500 (pane limit); retake at full resolution before publishing. This shot shows the coco_pharma database with a stale Egeria link ("element not found") left over from the Egeria reset; re-survey and re-publish before the retake, or pick another database. -->
![Resource Explorer's At a glance view of the coco_pharma database: schemas, tables, rows and size since the last survey](november-2026-resource-explorer.png)

**Egeria Advisor** now reads and authors dashboards held in Egeria, just as the Portal does, and publishes report specs. It runs Dr.Egeria as the signed-in user and refuses requests that carry no credentials. It shares the same feedback loop as Resource Explorer.

<!-- TODO-IMAGE: Egeria Advisor showing a dashboard sheet it read from Egeria. File: november-2026-egeria-advisor.png
     DRAFT shot taken 2026-11-13 as erinoverview on laz at 800x500 (pane limit); retake at full resolution before publishing. -->
![Egeria Advisor showing the Catalog Health sheet, held in Egeria and read as the signed-in user, with "not measured" where nothing was measured](november-2026-egeria-advisor.jpg)

Both applications are still a Tech Preview: they keep changing quickly, and your feedback shapes them. Try them, use the feedback buttons, and tell us what you would like next.

Learn more in the [Trellis repository](https://github.com/dwolfson/trellis) and the [Resource Explorer tutorial](https://github.com/dwolfson/trellis/tree/main/packages/resource-explorer/docs/tutorial).
<!-- TODO: confirm the Trellis repository link is the one to publish (dwolfson/trellis is public); link the 6.3 Tech Preview release once tagged: https://github.com/dwolfson/trellis/releases/tag/v6.3-tech-preview. -->

## pyegeria

pyegeria, the Python client for Egeria, has had 39 releases since 6.2.0 (6.2.1 to 6.2.39). The highlights:
<!-- TODO at the cut: extend to 6.2.42 (owner 2026-11-16: 6.2.42 is the stated floor everywhere). -->

- Clients and Dr.Egeria commands for Egeria 6.3's report specs, measurements and dashboards.
- Report specs that can be held in Egeria and run from plain pyegeria, checked when they load, with a reason given for any that cannot run.
- Counts that return "not measured" (`None`) rather than 0.
- A report spec can produce a standard document, starting with a DCAT-AP 3 catalog of a collection's Assets, checked against the DCAT-AP shapes.
- New Dr.Egeria commands for reference data, business capabilities, statements of applicability, survey reports and security findings.
- My Egeria (formerly My Profile) is now part of the production package.
- pyegeria runs on Python 3.14.

Install or upgrade with `pip install -U pyegeria`. The [pyegeria release notes](https://github.com/odpi/egeria-python/tree/main/docs/release-notes) describe each release.
<!-- TODO: link to the aggregate "6.2.0 → 6.2.x" page once it is merged. -->

## Future plans

Plans for the [next release](https://egeria-project.org/release-notes/next/) are open, and we welcome suggestions.

## Connecting with the project

Egeria is an open source project under LF AI & Data, and it grows through the people who use it and shape it. Whether you want to try Egeria on your own metadata, contribute code or content, or bring a hard problem to the discussion, we would be glad to hear from you.

- Talk with the team and other users on [Slack](https://slack.lfaidata.foundation){target=blank}.
- Watch demos and walkthroughs on [YouTube](https://www.youtube.com/@egeria-project){target=blank}.
- Follow the project on [LinkedIn](https://www.linkedin.com/company/egeria-project/){target=blank}.
- Read our blogs and articles on [Pragmatic Data Research, LTD](https://pdr-associates.com)

!!! info "Connecting with the community"
    Go to our [community guide](https://egeria-project.org/guides/community){target=blank} to find out more about the activities of the Egeria project and how to get involved.

--8<-- "snippets/abbr.md"
