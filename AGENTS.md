# Project handoff

This repository is an EPUB translation/production workspace, not a web app.

Before editing, read `WORKSPACE_SETUP.md`, then `SKILL.md` and `worklog.md` (§0 and
newest §8 entries). SKILL.md owns production rules; worklog.md owns editorial history.
The recovery report records discrepancies in the imported baseline; do not silently
change old chapters to make audit output green.

- Run tools from the repository root. Historical `/home/user/...` paths in the worklog
  map to this repository, `/home/user/Rumors_with_Taeyoen/`.
- `work_epub/` is the complete extracted editable book. Keep all assets and `mimetype`.
- Current cycle: reader-requested prose-first rewrite of chapters 307–308. See worklog
  §0/§8 and `reports/ch307_308_revision/`; baseline published308 commit a371947.
  Earlier chapter307/308 reports preserve the superseded layouts as history.
- Existing `raws/ch307_raw.txt` and `raws/ch308_raw.txt` are authoritative; do not overwrite.
- Raw-first custody, full source/output scans and question/phone audits remain mandatory.
  The reader has REPLACED style-block maximalism with prose-first restraint: use blocks
  only for substantial context that benefits from them; never pad to fill a panel.
  Preserve chapters1–306 and all existing assets/canon in this two-chapter revision.
- After producing and verifying each final EPUB, commit and push to the same session
  branch, verify remote HEAD, and provide the GitHub EPUB download link. Never force-push.
- `build_epub.py` overwrites the root deliverable. Never run it just to inspect the book.
- `workspace_audit.py` is read-only with respect to sources; it regenerates `reports/`.
  Keep production-cycle outputs in `reports/chNNN/` so the recovery baseline survives.
  It is not EPUBCheck, a semantic proofreader, or a substitute for the house gates.
- Preserve reader-supplied references in `uploads/`; do not replace their bytes.
- Dependencies and scratch work are ignored; the extracted tree and useful audit
  indexes are intentionally retained.
