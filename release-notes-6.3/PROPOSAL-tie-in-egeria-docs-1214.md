# Proposal: tie our 6.3 notes into Mandy's egeria-docs release notes

Status: proposal for the owner, 2026-11-16. Nothing changed in any repo yet; no PR open.
Source read: odpi/egeria-docs main `d55aa0cf` (#1214 "Release notes for 6.3 (part 1)", merged 13:08Z) and #1213.

## What Mandy's #1214 already covers

- `site/docs/release-notes/november-2026.md` is **the** November newsletter. It already has an
  Egeria Workspaces section (Resource Locator, grouped by purpose, lineage hop controls, dashboards and
  report specs held in Egeria, Airflow and Marquez, resizable columns, `egeria-upgrade-reset`) and a
  short pyegeria and Dr.Egeria section.
- `snippets/release-notes/6-3.md`: a two-paragraph summary (operations, performance, standards: DCAT,
  NIST, ISO/IEC 27001 statements of applicability, STRIDE, Open Lineage in PostgreSQL), then details
  and upgrade notes. It says nothing about pyegeria versions, Workspaces or Trellis.
- `overview.md`: 6.3 branch date 16 November, **release date 17 November**; 6.4 late December; 7.0 mid February 2027.
- Blogs 6 to 10. Blog 7 (security professionals) has a placeholder:
  `<!-- SCREENSHOT NEEDED: a statement of applicability with its linked controls ... in Egeria Explorer -->`.

So our own newsletter draft (`newsletter-november-2026.md`) now duplicates hers. Her text is the
published voice; ours should feed into it, not compete.

## Proposed changes

### 1. Newsletter: stop our standalone draft, add a small PR to hers

Retire `newsletter-november-2026.md` as a separate page. Instead, one small egeria-docs PR to
`november-2026.md` that adds only what is missing, in her style, without rewriting her text:

- **Egeria Workspaces section**, two or three bullets she doesn't have:
  - The Overview shows only what it measured (no sample numbers; "not measured" is said plainly).
  - The Catalog: a tab per kind of infrastructure, lists that page to the end.
  - Statements of applicability: the Coco sample (#881, merged), and the Egeria Explorer
    Statements of Applicability view (#882) **only if #882 merges first**. Each links to her
    "Statements of applicability" bullet in the security section.
- **A new short section "Tech Preview: Resource Explorer and Egeria Advisor"** (Trellis
  `v6.3-tech-preview`). Her newsletter doesn't mention Trellis at all; you decided it is
  released alongside 6.3 and is on the public demo. About five bullets, cut down from our draft.
- **pyegeria section**: one sentence with the version: "Install or upgrade with
  `pip install -U pyegeria`; 6.2.42 is the current release", and a link to the pyegeria release notes.
- **Images**: only if you want them; our draft shots are 800x500. Offer a full-size Statement of
  Applicability shot from Egeria Explorer for blog 7's placeholder (needs #882 merged and a retake).

### 2. Workspaces RELEASE_NOTES and CHANGELOG cut

- Add at the top: "For the Egeria 6.3 platform, see the [6.3 release notes](https://egeria-project.org/release-notes/latest/)
  and the [November 2026 newsletter](https://egeria-project.org/release-notes/november-2026/)."
- Where we describe a platform change (zones fail closed, 8-hop lineage limit, purposes, DCAT,
  Open Lineage in PostgreSQL), keep one line and link to her section instead of explaining it again.
- Use her terms in prose: "Open Lineage" (product names like the `OpenLineage` connector stay as is),
  "statement of applicability", "governance zones fail closed", "Resource Locator".
- Release date: use **17 November 2026** (her overview table) for `## [6.3]` and the tags, unless you
  want 16 November (the day the 6.3 image was pushed).
- Add #881 under Added; #882 only if merged.

### 3. Trellis CHANGELOG and RELEASE_NOTES

- Same top link to her 6.3 notes and blog 6.
- Add **Studio** (port 8840, trellis #1095), which isn't in our draft.
- Fix the pyegeria floor (see 5).

### 4. pyegeria aggregate page and one-page overview

- Extend to 6.2.40, 6.2.41, 6.2.42 (#593, #595, #598).
- Link to her 6.3 notes for the platform side.

### 5. pyegeria floor

Mandy's pages state no pyegeria version, so nothing conflicts. The code on main today:
workspaces quickstart `>=6.2.41`; trellis Resource Explorer `>=6.2.41`, Egeria Advisor and Studio `>=6.2.42`.
Still your call (asked earlier): state each repo's real floor, or 6.2.42 everywhere (needs a
workspaces floor PR).

### 6. Video script

Unchanged, but point its closing card at blog 6 and her 6.3 notes.

## Not doing

- Not editing her summary, details, upgrade notes or blogs, apart from offering the blog 7 screenshot.
- No PR to egeria-docs, workspaces, trellis or pyegeria until you say go.
