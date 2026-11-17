# Resource Explorer video: storyline and shot outline (draft)

About 2 minutes. It follows the Resource Explorer tutorial's story so the video and the tutorial reinforce each other
(`packages/resource-explorer/docs/tutorial/01-what-resource-explorer-is-for.md`; narration drafts for the tutorial
videos are in `docs/tutorial/narration/`).

## The story in one line

Peter Profile has a week to make the sources behind a clinical trial ones the catalog can vouch for, and to judge
one more before the team relies on it. Resource Explorer lets him look first, and catalog only what proves worth keeping.

## Cast and setting

- **Peter Profile**, information analyst at Coco Pharmaceuticals: the persona you sign in as.
- **Erin Overview**, the information architect, sets the task.
- The **Teddy Bear Drop Foot** trial. Three hospitals send weekly measurement files into the `loading_bay` folder;
  they're loaded into the `coco_pharma` database. A resent week arrives as `.restatement.csv`, and the original is kept.
- The new requirement: an outside auditor must be able to see the data is in good order without asking the team.

## The spine (the same four beats for every kind)

Look → judge → publish → ask. Show the spine in full once, on the database, then only the beat that's different for
each of the other kinds.

The three promises, said once and shown throughout:
1. Nothing reaches Egeria until you press **Publish**.
2. "Nothing found" and "not looked at yet" always look different.
3. Every answer can show where it came from.

## Outline

| # | Time | Scene | On screen | Narration idea |
|---|---|---|---|---|
| 0 | 0:00–0:10 | The problem | Erin's request; the trial's three sources sketched: database, drop folder, an open-source tool | "A regulator wants to see that the trial's data is in good order, without asking anyone. Peter has a week." |
| 1 | 0:10–0:20 | Sign in, find | Sign in as Peter; the investigation; the four kinds side by side: Databases, File systems, Repos, Open data | "Resource Explorer looks first, and catalogs only what's worth keeping." |
| 2 | 0:20–0:50 | **Database**: the full spine | `coco_pharma`: Scouting card and its questions with perspectives; run the overview survey (or open a stored one); table sizes, value profiles, quality checks; **6 Curate** → **Publish** → the check that it arrived; cut to the same table in the Portal | "Your questions decide what runs: cheap and broad first, deeper only where it's worth it." Then: "Nothing reaches Egeria until you press Publish, and then it checks it got there." |
| 3 | 0:50–1:10 | **File system** | `loading_bay`: the folder survey card "led by Egeria's Folder Survey"; the walk measures; a CSV profile; the `.restatement.csv` files visible; chat finds a passage in a document | "Egeria reads the folder and keeps the result. The resent weeks are right there, beside the files they replace." |
| 4 | 1:10–1:30 | **Repository** | `OpenLineage/OpenLineage`: the Scouting header tiles (language, stars, contributors, last pushed, size, health); the **SECURITY ? not read** tile; **Re-run…** | "Before adopting a tool, judge it. And see this: '? not read' isn't zero. Nobody has looked yet, and the screen says so." |
| 5 | 1:30–1:45 | **Open data** | Search an open-data portal (CKAN, DCAT-AP or Zenodo) with the price line shown before it runs; open a dataset; a field the source doesn't give shows as "not reported"; publish a single dataset and check it arrived; a DOI-only record showing what is known | "Public data comes with what the source says, and plainly marks what it doesn't." |
| 6 | 1:45–1:55 | **Ask** | Chat rail: a question across the trial's sources; the answer cites what's on screen and names what couldn't be determined | "Every answer can show where it came from." |
| 7 | 1:55–2:05 | Close | Erin's view in the Portal: the trial's sources catalogued; end card with the live demo and the six-part tutorial | "Look first. Catalog what proves worth keeping. Try it on the live demo." |

## Choices to make before filming

- **Which open-data source and dataset.** Pick a portal and a dataset that fit the trial, for example a public
  reference dataset the researchers want to compare against. Use one already registered on laz, so nothing new is
  written for the video.
- **Stored or live runs.** The tutorial uses stored surveys for OpenLineage and `coco_pharma`. Cutting to a stored
  result keeps the timing; a live run is honest but slow (the repository survey downloads the repository).
- **Publishing on laz.** Film a publish that has already been done, or run one only after a peer round. A new publish
  writes to the shared Egeria.
- **Persona.** The tutorial signs in as Peter Profile. The Portal video and the screenshots use Erin Overview. Using
  Peter here matches the tutorial; Erin can appear at the start and the end, as the person who asked.

## Shorter cuts

- **45 seconds:** scenes 0, 2 (database only) and 7.
- **Per kind, for the docs:** scene 1, then one of 2 to 5 in full, then 6. Each makes a 30–40 second clip for the top
  of its tutorial part.
