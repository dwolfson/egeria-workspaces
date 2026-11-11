<!-- DRAFT video script, made from overview-egeria-6.3.md. Target length about 7 minutes.
     Every screen is on the live demo (egeria.pdr-associates.com) or a local quickstart with Trellis.
     Before recording: sign in as a Coco persona with access to the dashboards folders (TODO: which persona;
     Jules Keeper, the CDO, has the CDO dashboard); check the four "useful" sheets and the consumer folders are seeded;
     check Resource Explorer has at least one surveyed PostgreSQL database and one published result.
     Timings are rough and cumulative. Narration is about 140 words a minute. -->

# Egeria 6.3: video script

**Title:** What's new in Egeria 6.3
**Length:** about 7 minutes
**Voice:** one narrator, plain and unhurried. Show, then say.

---

## Scene 1: Cold open (0:00–0:30)

**On screen:** Portal home page on the live demo, slowly scrolling over the tiles. Title card: "Egeria 6.3".

**Narration:**
> Egeria is an open source metadata platform. It keeps a shared, governed record of your data: what exists, what it
> means, where it came from, and who looks after it. People, tools and AI agents all work from the same record.
> Egeria 6.3 is about trusting that record. Let's look at what's new.

## Scene 2: The pieces (0:30–1:10)

**On screen:** A simple diagram (TODO: make one) with four boxes: Egeria platform at the bottom; Egeria Workspaces
and its Portal; Resource Explorer and Egeria Advisor; pyegeria. Then the Portal home again, pointing at the Resource
Explorer and Egeria Advisor tiles.

**Narration:**
> This release spans four projects. The Egeria platform does the work underneath. Egeria Workspaces is a
> ready-to-run environment with a browser Portal and demo content for a fictional company, Coco Pharmaceuticals.
> Resource Explorer and Egeria Advisor are two AI-assisted applications that sit alongside it. And pyegeria is the
> Python client that all of them use.

## Scene 3: Dashboards that live in Egeria (1:10–2:40)

**On screen:**
1. Portal → **Local Dashboards**. The folder tree on the left. Open a folder, then one of the four ready-made
   sheets (for example the repository trends sheet). Let the tiles load.
2. Hover a tile to show where its numbers come from.
3. Portal → **Egeria Explorer** → **Report Specs**. Show the **Used by** chips on a spec, then use the consumer
   filter to show only the specs Egeria Advisor uses.
4. Open a spec that cannot run and show the reason.

**Narration:**
> Until now, the Portal's dashboards and the reports behind them were files on a server. In 6.3 they live in Egeria.
> Here are the dashboards, organised in folders. Each sheet is an Egeria element with an owner, so it gets zones,
> history and search, like any other metadata.
> The reports that feed these tiles are report specs. Each tool has its own folder of specs, and Egeria Explorer
> shows which tools use each one. Here are the specs Egeria Advisor uses.
> A spec also says what it needs before it runs. If it can't run, it tells you why, instead of failing halfway.

## Scene 4: Numbers that say what they measured (2:40–3:40)

**On screen:**
1. Portal → **Egeria Overview**. Show a card marked "not measured" next to a measured one.
2. A count with a population label.
3. Resource Explorer: a database that has not been surveyed, showing "not established".

**Narration:**
> Zero and "we didn't check" are different answers. So are sixty and "at least sixty". We went through the Overview,
> the dashboards and the reports and kept those answers apart. A count that wasn't taken says so. A capped list says
> it's capped. Totals cover the whole repository.
> Resource Explorer follows the same rule. This database hasn't been surveyed, so its contents are "not established",
> not empty.
> When an AI reads these numbers and repeats them, that difference matters.

## Scene 5: Resource Explorer (3:40–5:10)

**On screen:**
1. Resource Explorer, Next UI, Dark look. A surveyed PostgreSQL database: the cards and tiles, At a glance.
2. The survey card for a Survey Definition: run line, history, the Cancel button.
3. The quality checks and value profile for one table.
4. Click **Publish**. Show the read-back confirming the elements arrived in Egeria. Then the same asset in the
   Portal's Egeria Explorer, with its zone.
5. Ask a question in chat about this database. Show the answer with its sources.
6. Rate the answer with a reason.
7. Switch the Look to Paper, then Light.

**Narration:**
> In October, Resource Explorer was an early preview. Now it surveys a resource, helps you decide what matters, and
> publishes the result into Egeria.
> Its surveys are registered with Egeria and run on Egeria's own engine, so each one has a history, and you can
> cancel it.
> For databases it goes deeper: table sizes, activity, value profiles and quality checks.
> When you publish, it checks that the result arrived. Here it is in Egeria, in the right zone.
> You can ask about the resource. Answers search the resource's own documents first and show where they came from.
> And if an answer is wrong, say why. An administrator reviews the feedback and can trace a problem back to a gap in
> the documents.

## Scene 6: Egeria Advisor (5:10–5:50)

**On screen:**
1. Egeria Advisor. Ask it to list the dashboards in Egeria; show the answer.
2. Ask it to show one sheet; show the same sheet as in Scene 3.

**Narration:**
> Egeria Advisor is a conversational assistant for Egeria. It now reads and authors the same dashboards as the Portal,
> so a dashboard built in one appears in the other. It acts as you, with your access, never as a service account.

## Scene 7: Easier to read, safer to run (5:50–6:30)

**On screen:**
1. Portal → Egeria Explorer, a busy element's detail panel. Relationships folded into families; open one.
2. Drag a column edge and a pane divider. Reload; the widths are remembered.
3. A terminal running `quick-start-local` and the start-up summary showing `localhost` URLs and the `--lan` hint.

**Narration:**
> Relationships are now grouped by purpose, such as composition, governance or operations, so a busy element is
> easier to read. Every column and pane can be resized, and the Portal remembers your widths.
> Running it yourself is safer by default: ports are local-only unless you open them, and the Portal sends credentials
> only to approved Egeria platforms.

## Scene 8: Learn it, and pyegeria (6:30–6:55)

**On screen:** Portal Docs → Tutorials overview page. Then a terminal: `pip install -U pyegeria`.

**Narration:**
> New tutorials cover saved queries, analytic functions, report specs and dashboards, each with worked examples.
> And pyegeria, the Python client, had thirty-six releases this cycle, adding everything you've just seen.

## Scene 9: Close (6:55–7:15)

**On screen:** Live demo sign-up page, then end card with: egeria.pdr-associates.com · egeria-project.org ·
Slack · YouTube.

**Narration:**
> You can try all of this in your browser, with nothing to install. The links are below. Tell us what works and what
> doesn't. Egeria grows through the people who use it. Thanks for watching.

---

## Shot list (for recording)

| # | App | Page / action | Scene |
|---|---|---|---|
| 1 | Portal | Home, tiles | 1, 2 |
| 2 | Portal | Local Dashboards: folder tree, a ready-made sheet | 3 |
| 3 | Portal | Egeria Explorer → Report Specs: Used by, consumer filter, a spec that can't run | 3 |
| 4 | Portal | Egeria Overview: "not measured" card, population label | 4 |
| 5 | Resource Explorer | Unsurveyed database ("not established") | 4 |
| 6 | Resource Explorer | Surveyed PostgreSQL database: cards, survey card, quality checks | 5 |
| 7 | Resource Explorer | Publish and read-back; same asset in Egeria Explorer | 5 |
| 8 | Resource Explorer | Chat answer with sources; rating with a reason; Look switch | 5 |
| 9 | Egeria Advisor | List dashboards; show a sheet | 6 |
| 10 | Portal | Detail panel with relationship families; resize and reload | 7 |
| 11 | Terminal | `quick-start-local` summary | 7 |
| 12 | Portal | Docs → Tutorials | 8 |
| 13 | Browser | Live demo sign-up page | 9 |
