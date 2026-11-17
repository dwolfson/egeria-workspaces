# Egeria 6.3 at a glance

**Egeria** is an open source metadata platform from LF AI & Data. It keeps a shared, governed record of an
organization's data: what exists, what it means, where it came from, who owns it and what has been promised
about it. People, tools and AI agents all read and write the same record.

Egeria 6.3 is delivered by several projects that work together:

| Project | What it is | Who it's for |
|---|---|---|
| **Egeria platform** | The metadata server and its connectors. | Everyone, underneath. |
| **Egeria Workspaces** (`odpi/egeria-workspaces`) | A ready-to-run environment: the platform, shared infrastructure, demo content for the fictional Coco Pharmaceuticals, and the **Portal**, a set of browser apps for exploring and governing metadata. | Anyone who wants to try Egeria or run it locally. |
| **Resource Explorer** and **Egeria Advisor** (`dwolfson/trellis`, 6.3 Tech Preview) | Two AI-assisted applications. Resource Explorer surveys resources that are not yet catalogued and helps you decide what to catalog. Egeria Advisor is a conversational assistant for Egeria. | Data stewards, analysts and developers. |
| **pyegeria** (`odpi/egeria-python`) | The Python client for Egeria, plus Dr.Egeria (metadata written as Markdown) and My Egeria (a terminal app). | Developers, notebook users, automation. |

## The story of this release

**1. Your dashboards and reports are metadata too.** Until now, the Portal's dashboards and the report specs behind
them were files on a server. In 6.3 they are kept in Egeria, in folders, with an owner. Each tool (the Portal, Egeria
Advisor, Resource Explorer, Jupyter and others) has a folder of the report specs it uses, and you can see which tools
use each spec. Because they are Egeria elements, dashboards and specs get zones, history and search like everything
else. A spec says what it needs before it runs, and if it can't run, it says why.

**2. A number should say what it measured.** "0" and "we didn't check" are different answers, and so are "60" and
"at least 60". The Portal, pyegeria and Resource Explorer now keep them apart: an unmeasured count is shown as not
measured, a capped list says it was capped, and totals cover the whole repository. (One caveat on Egeria 6.3: an unfiltered
count of data assets can come out low, so read it as "at least".) This matters most when an AI
reads the numbers and repeats them.

**3. A Tech Preview you can use.** Resource Explorer and Egeria Advisor are released together as the **6.3 Tech
Preview**: still changing quickly, and shaped by your feedback. Resource Explorer now publishes what it finds into Egeria, zoned and checked, and
its surveys run on Egeria's own engine. It analyses databases, files and open-data repositories more deeply, and it
learns from feedback: a rating can say why, an administrator triages it, and the document index can be rebuilt and
rolled back. Egeria Advisor reads and authors the same Egeria-held dashboards as the Portal.

**4. Easier to read, safer to run.** Relationships are grouped by purpose, so a busy element is easier to understand.
Every width in the Portal can be dragged. The demo is locked down by default: ports are local-only, workbenches have
an egress allow-list, credentials go only to approved platforms, and no request runs under someone else's identity.

**5. Easier to learn.** New tutorials and worked examples cover saved queries, analytic functions, report specs and
dashboards, and Resource Explorer has a six-part tutorial.

## By the numbers (October 9 to November 12, 2026)

- **Egeria Workspaces:** 217 merged changes.
- **Resource Explorer and Egeria Advisor:** more than 500 merged PRs.
- **pyegeria:** 43 releases, 6.2.1 to 6.2.42 and then 6.3.0, the release that matches Egeria 6.3.

## Try it

- **Live demo**, nothing to install: [egeria.pdr-associates.com](https://egeria.pdr-associates.com). Sign up, choose a
  Coco Pharmaceuticals persona, and open **Local Dashboards**, **Egeria Explorer**, **Resource Explorer** or
  **Egeria Advisor**.
- **Run it yourself:** [Egeria Workspaces](https://github.com/odpi/egeria-workspaces#getting-started) with Docker or
  Podman; add Resource Explorer and Egeria Advisor with [Deploying Trellis with the
  QuickStart](https://github.com/dwolfson/trellis/blob/main/docs/deploying-trellis-with-quickstart.md).
- **From Python:** `pip install -U pyegeria`.
- **Talk to us:** [Slack](https://slack.lfaidata.foundation), [YouTube](https://www.youtube.com/@egeria-project),
  [community guide](https://egeria-project.org/guides/community).

## Where to read more

- Newsletter: November 2026 on egeria-project.org.
- Egeria Workspaces: `RELEASE_NOTES.md` and `CHANGELOG.md` (6.3).
- Trellis: `RELEASE_NOTES.md` and `CHANGELOG.md` (6.3).
- pyegeria: `docs/release-notes/6.2.x-egeria-6.3.md`, plus one file per release.
