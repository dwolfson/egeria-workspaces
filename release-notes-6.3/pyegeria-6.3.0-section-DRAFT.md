<!-- SUPERSEDED 2026-11-16: merged into pyegeria-6.2.x-overview.md (now "pyegeria 6.3.0, with the 6.2 series that led to it"). Edit there. -->
<!-- pyegeria 6.3.0 tagged 2026-11-16: odpi/egeria-python#600, squash 3af20c48 = tag v6.3.0. Re-check items against 3af20c48 and cite #600; move into the page once the wheel is on PyPI (Coordinator signals). -->
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

### Paging on Egeria 6.3

- **pyegeria now knows which Egeria fixes a platform carries**, one version check per upstream fix, and trusts a read
  only on a platform that has every fix it needs (`pyegeria.core.paging`, `platform_fixes`). Egeria 6.3 carries
  both paging fixes: odpi/egeria#9453, for the find reads, and odpi/egeria#9454, for `get_relationships` and
  `get_related_elements`. Released Egeria from 6.3.0 on is trusted for both, since the V6.3 tag carries both fixes.
  On Egeria 6.3, pyegeria can tell when it has read to the end of those results. On older platforms, counts are
  reported as "at least N".
- **Known issue on Egeria 6.3:** a search for data assets with no filter can return fewer assets than the repository
  holds, so treat its count as a lower bound. <!-- EG-15 (Rocky, 2026-11-16: 440 of 1797 DataAssets missing from an
  unfiltered find_data_assets on released 6.3). Add the upstream issue link once one exists. -->
- **A find's count says "at least N" unless the end was confirmed.** `result_count(result)`
  (`pyegeria.view.format_set_executor`) gives the count, its wording, and the reason when it isn't final.
- **MCP report runs page up to their maximum rows** and include a count, so a filtered first page no longer reads as
  "nothing".

### Dr.Egeria and authoring

- **Limit Result by Status** is a list of element statuses, with lifecycle filters added.
- **Project Scope** maps to the project's `scope` property.
- **Default value overrides** are sent when the target type declares them.
- **Authoring validation is stricter**: the find method must suit the target type, and column keys are checked.
- **Deployment status matches Egeria** (PY-21). The fallback list of deployment statuses offered
  `REJECTED_FOR_DEPLOYMENT`; Egeria's value is `REJECTED`.
- **Drafts are listed correctly on a live Egeria.** Listing and pruning drafts used to find none on a real server.
  They now read each kind by type, filtered by the author's zone.
- **Egeria 6.3's type system**: the properties catalog is regenerated from Egeria, and the `queries` attribute is no
  longer sent or accepted on schema types.

### Planned for pyegeria 6.4 or the next release


- **`load_egeria_report_specs` will be removed in pyegeria 6.4 or the next release.** It has been deprecated since 6.2.42 (see PR) and
  logs a warning once. Report specs held in Egeria load through the spec cache (`pyegeria.view.egeria_spec_cache.sync_report_specs`).
- **pyegeria 6.4 or the next release drops the default password** and any built-in identity, except in a demo profile
  that is named explicitly.
