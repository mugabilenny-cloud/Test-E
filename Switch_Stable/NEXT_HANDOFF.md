# Switch — Next Handoff
**Date:** 11 September 2026

## Build status
The ten wiring gaps from the previous handoff have been implemented in this repository.

1. **Home** — signed-in `user_id` is passed to active-course/history calls; recent entries use `resource_id`; course tiles are styled; sign-out is available under Account.
2. **My Courses** — signed-in `user_id` is passed to the active-course loader.
3. **Course Detail** — leaf resources are grouped by `Class Title` into labeled topic sections through `links_for_node_grouped()`.
4. **Saved** — signed-in saves are loaded per user; video saves use the inline video card.
5. **Viewer** — YouTube resources render inline; Viewer opens are recorded once per Streamlit session/resource; saves are per user.
6. **Search** — hierarchy match metadata (`matched_level`) is surfaced in the course-search result shape.
7. **Sign out** — destroys the server-side session token, removes the query parameter, clears the cached user and returns to Auth.
8. **History video metadata** — history now retains `youtube_video_id` when available, with Viewer/card fallback re-parsing from the URL.
9. **Live-readiness checks** — all Python files compile; importer runs; data store loads; local Streamlit process can be started and health-checked. Browser-level manual clicking still depends on the deployment/browser environment.
10. **Documentation** — the stale grouped-method naming is removed from the local implementation.

## Verification performed
- `py_compile` was run across every Python file in the package.
- The bundled spreadsheet was imported successfully.
- Deterministic node/link IDs were generated.
- Auth logic was checked for password hashing, duplicate-user rejection, login verification, session creation, expiry and destruction.
- Per-user saved/history storage was checked for user isolation and deduplication.
- Topic grouping and hierarchy search were checked against the imported tree.
- YouTube ID parsing is implemented for `watch?v=`, `youtu.be/`, and `/embed/` URL forms.

## Important data discrepancy
The prior 11 September handoff reported **24 nodes / 157 links and 30 real YouTube URLs**. The packaged workbook available for this build currently imports to the older data state and has no populated YouTube URLs. This handoff deliberately does not invent replacement URLs. When the 157-link workbook is available, replace `repo_5.xlsx` and run:

```bash
python tools/import_content.py repo_5.xlsx
```

## Scope preserved
`pages/4_Upload.py` remains a UX placeholder. No student write path was added. The local build remains a prototype; JSON files are not a substitute for a transactional production backend under concurrent public traffic.
