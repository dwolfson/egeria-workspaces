# Plan: our three 6.3 release-note outputs, fitted to Mandy's egeria-docs #1214

Status: plan for the owner, 2026-11-16. Nothing changed in any repo; no PR open. Every PR waits for the owner's go.
Source read: odpi/egeria-docs main `d55aa0cf` (#1214 "Release notes for 6.3 (part 1)", merged 13:08Z; also #1213).

## What Mandy's material covers, and the gap

- `site/snippets/release-notes/6-3.md` (shown by `latest.md`): summary, about 45 "Details of this release"
  boxes about the platform, then Upgrade notes. **Unlike 6.1 and 6.2, it has no boxes for our work yet.**
  In 6.2 the same file had "AI applications on Trellis", "Enhancements to the Egeria Workspaces",
  "Enhancements to Dr.Egeria and pyegeria" and "Refreshed Coco Pharmaceuticals content", placed just
  before Upgrade notes. That is the slot for ours.
- `site/docs/release-notes/november-2026.md`: the newsletter. It already has short Egeria Workspaces and
  pyegeria sections. It has nothing on Trellis.
- `overview.md`: 6.3 branched 16 November, **released 17 November**.
- Blogs 6 to 10: the 6.3 release, security professionals, data mesh, business flows from lineage, DCAT.
  Blog 7 has an empty placeholder: "SCREENSHOT NEEDED: a statement of applicability ... in Egeria Explorer".
- No pyegeria version appears anywhere in her pages.

## Output 1: into egeria-docs (one PR to odpi/egeria-docs)

**A. `site/snippets/release-notes/6-3.md`**: four new `??? functional` boxes before `### Upgrade notes`, in the 6.2
layout and her voice (short, plain, linking to `/user-interfaces/...` pages):

1. **"Enhancements to the Egeria Workspaces"**:
   - Dashboards and report specs held in Egeria, in folders;
   - the Overview shows only what it measured;
   - relationships and classifications grouped by purpose (links to her purpose concepts);
   - Resource Browser and Resource Locator;
   - The Catalog tabs;
   - lineage hop limit and the Expand viewer;
   - resizable panes;
   - Airflow and Marquez;
   - `egeria-upgrade-reset`.
   Statements of applicability go in two places: the Coco sample (#881, merged) here, and the
   Explorer view (#882) only if it merges first.
2. **"Enhancements to Dr.Egeria and pyegeria"**:
   - new command families: statements of applicability, business capability, report specs, measurements,
     dashboards, zone membership;
   - DOCUMENT and DCAT report output;
   - paging that completes and says when a result was capped;
   - the authoring API;
   - "pyegeria 6.2.42 is the current release".
3. **"AI applications on Trellis (6.3 Tech Preview)"**:
   - Resource Explorer publishes to and surveys through Egeria;
   - Egeria Advisor;
   - the new Studio authoring surface;
   - the same Tech Preview caveat as 6.2;
   - tag `v6.3-tech-preview`.
4. **"Refreshed Coco Pharmaceuticals content"**:
   - Chief Data Officer dashboard;
   - the statement of applicability sample (#881);
   - sustainability reference data;
   - Airflow pipelines.

Plus two Upgrade-notes bullets:
- The minimum pyegeria versions per repo (see "Decisions").
- Run `egeria-upgrade-reset` for the quickstart.

**B. `site/docs/release-notes/november-2026.md`**: small additions only; her text stays as written.
- Add a short **"Tech Preview: Resource Explorer and Egeria Advisor"** section after Egeria Workspaces.
- Add one statement of applicability bullet to her Workspaces list, linked to her security section.
- Add a version line to her pyegeria section.

**C. Blog 7 screenshot (taken now, draft):** `images/november-2026-statement-of-applicability.jpg` (header and
implementation summary tiles) and `...-controls.jpg` (the filterable controls table). Both are 800x600, taken
read-only on laz Egeria Explorer (#882 at a69e7084) with Mandy's Coco ISMS sample. They were taken as **Gary Geeke**,
the persona already signed in, and his badge shows in the header: crop it out, or retake as erinoverview at full size.
Offer them to Mandy in the egeria-docs PR or in a note. #882 isn't merged, so the caption says "Egeria Explorer
(Egeria Workspaces)" and claims nothing about a release.

New in this PR: only our components. Linked, not repeated: everything platform-side (zones, purposes, DCAT,
Open Lineage, the nannies, security pack) points at her boxes and blogs.

## Output 2: in our repos (one PR each)

Each of these opens with "For the Egeria 6.3 platform, see the
[6.3 release notes](https://egeria-project.org/release-notes/latest/) and
[blog 6](https://github.com/odpi/egeria-docs/tree/main/blogs/blog-6-egeria-6-3-release)".
Platform items shrink to one linked line each. They use her terms: "Open Lineage" in prose,
"statement of applicability", "governance zones fail closed".

| Repo | Files | Repo-specific detail kept |
|---|---|---|
| odpi/egeria-workspaces | `RELEASE_NOTES.md` new 6.3 section; `CHANGELOG.md` `[Unreleased]` cut to `[6.3]`; tag `v6.3` | Portal changes by app, PR list, upgrade notes. The quickstart needs **pyegeria 6.2.42 or later** (needs a floor PR: the Dockerfiles are still `>=6.2.41`). Adds the quickstart re-pin to `odpi/egeria-platform:6.3`, #881, and #882 if merged. |
| dwolfson/trellis | `CHANGELOG.md` `[6.3 Tech Preview]`; `RELEASE_NOTES.md`; tag `v6.3-tech-preview` | Resource Explorer, Egeria Advisor and **Studio** (new: #1095, port 8840). Needs **pyegeria 6.2.42 or later** (Resource Explorer's pyproject is still `>=6.2.41`; raise it to match). Adds `EMBEDDING_DEVICE` gone and the Postgres password change. |
| odpi/egeria-python | new `docs/release-notes/6.2.x-egeria-6.3.md` | The aggregate of 6.2.1 to **6.2.42** (adds 6.2.40 #593, 6.2.41 #595, 6.2.42 #598). Behaviour changes and the upgrade table. |

Our standalone newsletter draft (`newsletter-november-2026.md`) is retired: its content moves into Output 1B and
Output 3. The one-page overview stays as a local working page and is not published.

## Output 3: a video and a companion blog (complement, not duplicate)

**In one line:** a 7-minute narrated screen-recording video, "A tour of the Egeria 6.3 Portal: Explorer,
dashboards and Dr.Egeria", with a matching written blog (blog 11 in `odpi/egeria-docs/blogs/`). It shows the tools
her blogs 6–10 describe, and doesn't repeat her platform story. Where the video lives is your call: the Egeria
YouTube channel (linked from her newsletter), or a link from blog 11.

Her blogs explain the platform. Ours shows the tools: **"A tour of the Egeria 6.3 Portal: Explorer, dashboards
and Dr.Egeria"**.

- **Video**: rework `video-script-egeria-6.3.md` into a tour, about 7 minutes, as Erin Overview, recorded on laz
  or the live demo.
  1. Portal home.
  2. **A statement of applicability in Egeria Explorer**: Mandy's Coco ISMS sample, the #882 view. This ties
     into her blog 7.
  3. The same statement of applicability written as a Dr.Egeria document, from #881's workbook.
  4. Relationships and classifications grouped by purpose, linked to her concepts.
  5. Dashboards and report specs held in Egeria.
  6. The Overview's honest numbers.
  7. Resource Explorer and Egeria Advisor, 60 seconds, as a Tech Preview.
  8. Close, pointing at her blogs 6 to 10 for the platform story.
  The current scenes on platform features (zones, Open Lineage) are cut, because her blogs cover them.
- **Blog**: `blogs/blog-11-touring-the-egeria-portal/README.md` in egeria-docs, the written form of the tour,
  with the screenshots. It goes in the same PR as Output 1, or a separate one, as Mandy prefers.
- **Retakes needed**: full-size shots. The statement of applicability view needs #882 merged. The Resource
  Explorer shot comes after the Resource Explorer recovery. Crop the Prefect banner.

## Decisions needed from the owner

1. **The plan as a whole:** go, or change parts.
2. ~~pyegeria floor~~ **Decided 2026-11-16: 6.2.42 everywhere.** The workspaces quickstart and trellis Resource
   Explorer code floors must be raised to match before the notes go out.
3. **Release date for changelog headings and tags:** 17 November (her overview table), or 16 November (the
   day the image was pushed).
4. **Quickstart re-pin PR** to `odpi/egeria-platform:6.3`: should I open it?
5. **#882:** wait for it to merge before the egeria-docs PR, or go without it and add it later.
6. **egeria-docs layout:** check with Mandy before the PR that our four boxes and the blog 11 slot suit her.
   This is a question for you to pass on; I won't contact her.

## Order once approved

1. Do the cut in the worktree: run the merge check, refresh the stats, cover 6.2.40 to 6.2.42 and Studio.
2. Draft Output 1 and Output 2.
3. Show you the diffs.
4. Open the PRs.
5. Tag on the release date.
6. Rework the video script and write the blog draft.
7. Retake the screenshots.

## Owner decisions, 2026-11-16

1. Plan: **go as written** (outputs 1–3; diffs shown before any PR).
2. pyegeria floor: **6.2.42 everywhere**. I open the two code-floor PRs (workspaces quickstart Dockerfiles; trellis
   Resource Explorer pyproject), shown to the owner first.
3. Release date: **17 November 2026** for changelog headings and the `v6.3` / `v6.3-tech-preview` tags.
4. #882: **wait** for it to merge before the egeria-docs PR.
5. Quickstart re-pin to `odpi/egeria-platform:6.3`: **yes, open it** (shown first).
6. Mandy: **the owner asks her** about the four boxes and blog 11; I wait for his word.
7. Blog 7 screenshots: **retake full size as erinoverview** and add them in our egeria-docs PR.
8. Video: **Egeria YouTube channel**; blog 11 and the newsletter link to it.
