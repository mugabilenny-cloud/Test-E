# Switch — stable local build

This build closes the ten gaps in the 11 September 2026 handoff while preserving the six-screen Switch navigation. It uses the local JSON data/auth layer and requires no external database at runtime.

## Run
```bash
pip install -r requirements.txt
python tools/import_content.py repo_5.xlsx
streamlit run app.py
```

## Data note
The packaged `repo_5.xlsx` is the latest matching workbook available to this build. It does **not** contain the 30 populated YouTube URLs described in the 11 September handoff, so the package does not fabricate those URLs. Replace the workbook with that later version when available and rerun the importer.

## Prototype limitation
JSON storage is appropriate for a small prototype/single-process deployment. A public multi-user deployment should move content, authentication, history and saved items to a transactional backend.
