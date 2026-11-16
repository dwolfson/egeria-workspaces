<!-- DRAFT, 2026-11-16: the pyegeria 6.3.0 section, held until 6.3.0 is on PyPI (Coordinator owns the release; owner gives the go).
     Built from the code diff v6.2.42..origin/release/next fb5e655a, plus PY-21 (ca935426) and the #9454 release floor
     (4b2eccd5) on the Coordinator's prep/6.3.0 branch, whose next.md (55fb4d3c) is now trimmed to match. Originally NOT from next.md:
     next.md was not reset after 6.2.42, so it also lists items that already shipped in 6.2.42 (NO_PASSWORD and
     helper_client, can_edit, used_by, AuthoringRefused.answer, the per-identity spec cache, the
     load_egeria_report_specs deprecation). Those belong in the 6.2.40–6.2.42 part of the page.
     When 6.3.0 is cut: retitle the page "pyegeria 6.3.0 (with the 6.2.x series that led to it)", put this section
     first, re-check every item against the tagged commit, and add the PR number. -->

## pyegeria 6.3.0

pyegeria 6.3.0 is the release that matches Egeria 6.3. It follows 6.2.42 and adds the changes below. If you're coming
from an earlier 6.2 release, the rest of this page describes the 6.2 series that led up to it.

```bash
pip install -U pyegeria
```

### Paging you can trust on Egeria 6.3

- **pyegeria now knows which Egeria fixes a platform carries**, one version check per upstream fix, and trusts a read
  only on a platform that has every fix it needs (`pyegeria.core.paging`, `platform_fixes`). Egeria 6.3 carries
  both paging fixes: odpi/egeria#9453, for the find reads, and odpi/egeria#9454, for `get_relationships` and
  `get_related_elements`. Released Egeria from 6.3.0 on is trusted for both, since the V6.3 tag carries both fixes.
  On Egeria 6.3, results from those reads can be confirmed complete. On older platforms they are reported as
  "at least N".
- **A find's count says "at least N" unless the end was confirmed.** `result_count(result)`
  (`pyegeria.view.format_set_executor`) gives the count, its wording, and the reason when it isn't final.
- **MCP report runs page up to their maximum rows** and include a count, so a filtered first page no longer reads as
  "nothing".

### Dr.Egeria and authoring

- **Limit Result by Status** is a list of element statuses, with lifecycle filters added.
- **Project Scope** maps to the project's `scope` property.
- **Default value overrides** are sent when the target type declares them.
- **Authoring validation is stricter**: the find method must suit the target type, and column keys are checked.
- **Status values match Egeria** (PY-21). The fallback list of deployment statuses offered `REJECTED_FOR_DEPLOYMENT`;
  Egeria's value is `REJECTED`. The built-in report specs for Actor Manager, Feedback and Projects now offer the
  `FOR_INFO` activity status.
- **Drafts are listed correctly on a live Egeria.** Listing and pruning drafts used to find none on a real server.
  They now read each kind by type, filtered by the author's zone.
- **Egeria 6.3's type system**: the properties catalog is regenerated from Egeria, and the `queries` attribute is no
  longer sent or accepted on schema types.

### Coming in pyegeria 7 (expected early January 2027)

- **`load_egeria_report_specs` will be removed.** It has been deprecated since 6.2.42 (see PR) and logs a warning
  once. Report specs held in Egeria load through the spec cache (`pyegeria.view.egeria_spec_cache.sync_report_specs`).
- **No default password or built-in identity**, except in a demo profile that is named explicitly.
