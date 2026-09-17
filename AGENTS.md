# Project handoff

This repository is an EPUB translation/production workspace, not a web app.

Before editing, read `WORKSPACE_SETUP.md`, then `SKILL.md` and `worklog.md` (§0 and
newest §8 entries). SKILL.md owns production rules; worklog.md owns editorial history.
The recovery report records discrepancies in the imported baseline; do not silently
change old chapters to make audit output green.

- Run tools from the repository root. Historical `/home/user/...` paths in the worklog
  map to this repository, `/home/user/Rumors_with_Taeyoen/`.
- `work_epub/` is the complete extracted editable book. Keep all assets and `mimetype`.
- Chapter 307 is the current production cycle; consult worklog §0/§8 for its final
  archive seal and `reports/ch307/` for review/verification. Published 306 baseline:
  commit 060db57. Retain earlier raw versions and recovery/production reports.
- `raws/ch307_raw.txt` is the current raw-first source. Await a new task/raw for 308.
- Raw-first, Deep Scan + Deep Thinking, contextual style-block maximalism and pre-build
  question-mark/phone-call audits remain mandatory. Preserve chapters 1–306 and canon.
- After producing and verifying each final EPUB, commit and push to the same session
  branch, verify remote HEAD, and provide the GitHub EPUB download link. Never force-push.
- `build_epub.py` overwrites the root deliverable. Never run it just to inspect the book.
- `workspace_audit.py` is read-only with respect to sources; it regenerates `reports/`.
  Keep production-cycle outputs in `reports/chNNN/` so the recovery baseline survives.
  It is not EPUBCheck, a semantic proofreader, or a substitute for the house gates.
- Preserve reader-supplied references in `uploads/`; do not replace their bytes.
- Dependencies and scratch work are ignored; the extracted tree and useful audit
  indexes are intentionally retained.
