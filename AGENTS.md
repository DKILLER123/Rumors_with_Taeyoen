# Project handoff

This repository is an EPUB translation/production workspace, not a web app.

Before editing, read `WORKSPACE_SETUP.md`, then `SKILL.md` and `worklog.md` (§0 and
newest §8 entries). SKILL.md owns production rules; worklog.md owns editorial history.
The recovery report records discrepancies in the imported baseline; do not silently
change old chapters to make audit output green.

- Run tools from the repository root. Historical `/home/user/...` paths in the worklog
  map to this repository, `/home/user/Rumors_with_Taeyoen/`.
- `work_epub/` is the complete extracted editable book. Keep all assets and `mimetype`.
- Chapter 303 is now produced under the reader's subsequent authorization; consult
  worklog §0/§8 for the final archive seal and `reports/ch303/` for its review.
- Preserve both `raws/ch303_raw.txt` and `raws/ch303_user_resubmitted_raw.txt`. The
  latter is this cycle's translation source. Await a new task/raw before chapter 304.
- Raw-first, Deep Scan + Deep Thinking, style-block maximalism, and question-mark/
  phone-call audits remain mandatory; preserve chapters 1–302 and settled canon.
- `build_epub.py` overwrites the root deliverable. Never run it just to inspect the book.
- `workspace_audit.py` is read-only with respect to sources; it regenerates `reports/`.
  Keep production-cycle outputs in `reports/chNNN/` so the recovery baseline survives.
  It is not EPUBCheck, a semantic proofreader, or a substitute for the house gates.
- Preserve reader-supplied references in `uploads/`; do not replace their bytes.
- Dependencies and scratch work are ignored; the extracted tree and useful audit
  indexes are intentionally retained.
