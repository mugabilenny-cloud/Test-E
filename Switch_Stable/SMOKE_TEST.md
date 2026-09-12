# Smoke test

1. Run the SQL migration.
2. Create an admin auth user and set `app_metadata.role` to `admin`.
3. Configure `.streamlit/secrets.toml`.
4. Run `streamlit run app.py`.
5. Confirm Home loads and a device token appears in the query string.
6. Confirm root nodes appear in My Courses.
7. Search for a course and drill down to a leaf.
8. Confirm active links appear as resources.
9. Open a resource, confirm the real URL is available, then Save it.
10. Open Saved and confirm the bookmark persists after a rerun/browser reload using the same device URL.
11. Open the admin app, add a link, and verify it appears in the student app without UI changes.
12. Create an ad/notification and verify it appears through the existing Home feed/popup slots.
