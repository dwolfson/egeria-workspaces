"""
SPDX-License-Identifier: Apache-2.0
Copyright Contributors to the ODPi Egeria project.

Stable, known-good entities from the Coco Pharmaceuticals seed data
(`CocoComboArchive`, one of the 11 .omarchive files loaded into
`qs-metadata-store` whenever its Postgres schema is empty — see
`compose-configs/egeria-quickstart/servers/qs-metadata-store/config/
qs-metadata-store.config`). Archive-seeded GUIDs and qualifiedNames are fixed
by the archive itself, so these anchors are safe to assert on exactly as long
as nothing has rewritten the archive content packs.

If a content-pack update ever changes one of these entities, the fix is to
re-derive the anchor from the live `/api/...` response (see each anchor's
`# verified against: <endpoint>` comment) and update this file — NOT to loosen
the assertions in the tests that consume it.
"""

# NOT archive-seeded, unlike the header assumes: this WorkItemList and its Projects are loaded by Dr.Egeria
# from exchange-quickstart/loading-bay/dr-egeria-inbox/Local Dashboards/LOCAL_DASHBOARDS_ROADMAP.dr-egeria.md,
# so Egeria assigns new GUIDs whenever the platform is reset and the document re-run. qualifiedNames,
# names, category and membership are stable; GUIDs are not. Re-derived 2026-11-16 after the reset (old
# WorkItemList guid 0affb580-fa81-4d00-9438-b26faf11845d no longer exists).
# verified against: GET /api/collections/14fb3765-9b73-4a6c-933b-db18c220678d (2026-11-16)
WORK_ITEM_LIST = {
    "guid": "14fb3765-9b73-4a6c-933b-db18c220678d",
    "typeName": "WorkItemList",
    "displayName": "Local Dashboards - Next Steps",
    "qualifiedName": "Coco Pharmaceuticals::WorkItemList::Local-Dashboards---Next-Steps::1.0",
    "category": "Roadmap",
    "status": "ACTIVE",
    # (guid, displayName, typeName) for every collectionMember — order not
    # asserted (Egeria doesn't guarantee member ordering), membership set is.
    "members": {
        ("d3ee9e60-2351-432b-b002-c66a5b571670", "Add drill-click parity for Vega bar/line charts", "Project"),
        ("b649fed6-df76-4bdd-a8dd-a216b25ede8d", "Unblock find_method for Dashboard Sheet commands", "Project"),
        ("486aa04e-63fb-48a0-85c8-36e207559f8d", "Build Egeria Advisor dashboard editor (NEXT-13)", "Project"),
        ("1b10cb3c-da69-4096-ab5e-2a689f67e728", "Render nested Dashboard Sheets inline", "Project"),
        ("c1be70b4-2909-41db-b9b9-3ffd107bcefb", "Wire funnelChart into AI & Context Intelligence tile", "Project"),
    },
}

# One of WORK_ITEM_LIST's members — used by tests/browser/ to reproduce the
# 2026-07-31 Collections-vs-Digital-Products routing bug end to end: open
# this project, click "View" on its WORK_ITEM_LIST membership, and confirm
# the destination is the Collections tab (not Digital Products).
# verified against: GET /api/collections/14fb3765-9b73-4a6c-933b-db18c220678d collectionMembers (2026-11-16)
NEXT_13_PROJECT = {
    "guid": "486aa04e-63fb-48a0-85c8-36e207559f8d",
    "displayName": "Build Egeria Advisor dashboard editor (NEXT-13)",
    "qualifiedName": "Build Egeria Advisor dashboard editor (NEXT-13)::1.0",
}
