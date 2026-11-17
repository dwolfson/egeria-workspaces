# PR prep notes (internal; not for any PR)

## workspaces RELEASE_NOTES (header removed from the draft 2026-11-17, Architect W4)

<!-- DRAFT: new top section for odpi/egeria-workspaces RELEASE_NOTES.md.
     At release: put this above "# Egeria Workspaces 6.2", demote 6.2's H1 if the file should hold several
     releases, and REMOVE the 6.2 file's "## Since 6.2 (unreleased, on main)" section (folded in below).
     Move 6.2's "Report specs held in Egeria are read from the Portal's consumer folder" upgrade note here
     (it describes 6.3 behaviour). Stats are from 903e8eeb (#619, 2026-10-09) to 3b8ac7e2 (#857, 2026-11-12);
     refresh them at the cut. Release tentatively Monday 2026-11-16, alongside Egeria 6.3 (owner, 2026-11-11);
     v6.2 is tagged at 903e8eeb. These notes are also our piece of the Egeria project's 6.3 release notes.
     Resource Explorer and Egeria Advisor ship as the "6.3 Tech Preview" (dwolfson/trellis). -->


## workspaces CHANGELOG: not itemised (moved out of the draft 2026-11-17, Architect W4)

### Not itemised

Docs-only PRs (design notes and Portal Docs reorganisation: #649, #683, #728, #778, #782, #786, #787, #792, #794,
#797, #799, #813), CI chores (#744, #747, #768, #779) and the "keep RELEASE_NOTES per release" note. Dependabot bumps after #830 (#834–#837, #839, #841–#843) go under the existing
Dependencies entry.

The `--lan` entry: if the existing `[Unreleased]` already lists #687, keep one entry (under Security).

## trellis-RELEASE_NOTES.md: comments moved out of the draft 2026-11-17

<!-- DRAFT: new file RELEASE_NOTES.md at the root of dwolfson/trellis, mirroring egeria-workspaces' RELEASE_NOTES.md.
     Range b74b07f9 (2026-10-09) to 73738df8 (#1086, 2026-11-12), plus #1095/#1099 by hand. Refresh the stats at the cut.
     Owner decisions: label "6.3 Tech Preview", tag v6.3-tech-preview, released with Egeria 6.3 on Tuesday
     2026-11-17; RE and EA are on the public demo. -->

## trellis-CHANGELOG.md: comments moved out of the draft 2026-11-17

<!-- DRAFT: new file CHANGELOG.md at the root of dwolfson/trellis.
     Baseline b74b07f9 (2026-10-09, the October 2026 newsletter) to 73738df8 (#1086, 2026-11-12).
     Owner decision 2026-11-11: the release is "6.3 Tech Preview", tagged and released (GitHub release) to coincide
     with the Egeria 6.3 release on Tuesday 2026-11-17 (owner, 2026-11-16). Tag name: v6.3-tech-preview (owner, 2026-11-13).
     Package versions (resource-explorer 0.1.0, egeria-advisor 0.1.2, ...) are left as they are. -->
<!-- Folded in 2026-11-17: #1087–#1103 (all merged; #1090 and #1095 were already in). Was: fold in #1087–#1102. #1099 (RE pyegeria floor 6.2.42, 825e496e) and #1100 (RE fix batch TR-1/2/15/22/24) merged 2026-11-16; #1101 (floor 6.3.0 for RE/EA/Studio/trellis-auth) merged 16:50Z, main 34dbddb5; #1102 (TR-27 docs) merged 17:21Z, 389a14ff. #1100 described from its PR and commits. -->

## pyegeria page: comments moved out of the draft 2026-11-17

<!-- DRAFT: new file docs/release-notes/6.3.0-egeria-6.3.md in odpi/egeria-python (was planned as 6.2.x-egeria-6.3.md).
     pyegeria 6.3.0 = odpi/egeria-python#600, squash and tag v6.3.0 = 3af20c48, on PyPI 2026-11-16 15:50Z.
     The 6.2 part covers v6.2.0 (c9dc7a43, 2026-10-08) to v6.2.42 (9b3eb8e9, 2026-11-15). Numbers are PRs in
     odpi/egeria-python. 6.2.40–6.2.42 written 2026-11-17 from #593, #595, #598 and docs/release-notes/6.2.40.md;
     there are no 6.2.41/6.2.42 note files (their notes were in next.md at v6.2.42). -->
<!-- EG-15 (Rocky, 2026-11-16: 440 of 1797 DataAssets missing from an
  unfiltered find_data_assets on released 6.3). Add the upstream issue link once one exists. -->

## overview: comments moved out of the draft 2026-11-17

<!-- DRAFT: cross-repo overview of the Egeria 6.3 release, about one page, for someone new to the project.
     It is also the source for video-script-egeria-6.3.md. -->

## Release gate R2 (2026-11-17)
Dan, typed in the Architect's session, relayed verbatim: "Merge #889 before the 6.3 release - will be tomorrow".
No security-warning line. Once #889 merges, before the release PRs, un-stage the three #889 blocks:
the Resource Locator line (RELEASE_NOTES, Nov 8-16 section), the provisioner text in upgrade step 5, and the
CHANGELOG Security + Added entries. R1 and R3 fixed in f2258115.

## Resource Locator L6 (live on laz 2026-11-17 04:23:20Z, Coordinator)
Browse lists gain a Lens filter (inside / outside / cannot be compared) and a "Data scope recorded / none recorded"
facet. Goes to odpi in a PR after #889 merges, so probably not in the 6.3 release. If that PR merges before the
release PRs, add it to the Resource Locator line and the CHANGELOG Added entry. Not in any draft yet.

**Done 2026-11-17:** #889–#892 merged upstream (13:06–13:07Z, 97ecd7ef). The #889 and #892 blocks are un-staged,
and #890/#891 entries added. Before the PRs, recount the contributor commit numbers in the "Thank you" line
(they predate these merges).
Recount once, after the last merge before the release PRs, over one window for all of: the RELEASE_NOTES "In numbers"
line (377 commits / 217 PRs), the overview's "By the numbers (October 9 to November 12)" heading and figures, and the
"Thank you" counts (Architect R2, 5bd4437f read-back).

**#893 staged 2026-11-17** (bundle/2026-11-17-rl-followups f8cdb91e): four STAGED blocks, two in RELEASE_NOTES
(Locator line after #889's; freshstart line under Other changes) and two in the CHANGELOG (Added; Fixed). #893 also
carries the L6 features above (Lens filter on Browse, "no data scope recorded" count), so they're covered by it.
Un-stage all four when it merges, then do the recount.
