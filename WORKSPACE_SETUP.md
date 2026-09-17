# Workspace ready — Peninsula, through Chapter308, prose-first revision

**Workspace:** `/home/user/Rumors_with_Taeyoen`  
**Repository:** `DKILLER123/Rumors_with_Taeyoen`  
**Session branch:** `arena/01a09949-rumors-with-taeyoen`

## Current production state — rewrite of307–308

Both chapters rewritten from untouched archived raws at the reader’s request. Prose-first
restraint now supersedes style-block maximalism: sufficient real context only, no filler
or panel quota.307has2blocks instead of40;308has5instead of44. All ordinary narrative,
thoughts, dialogue and planning restored to flowing prose. All source events and System
mechanics retained, including the established canon corrections. Existing images preserved.

Pre-build log recorded; chapter/source/punctuation/repeat/XML/CSS and390/800browser checks
complete. Revised archive seal verified. Current evidence: `reports/ch307_308_revision/`; earlier
307/308reports are historical. Only307,308and OPF modification timestamp change in-book.
All306other chapters, assets/styles, references and navigation remain byte-identical.
308chapters /414payloads /411manifest /312spine /311NCX /314navli;76images /20fonts;
19characters /61glossary; next image id-54. No EPUBCheck/all-reader certification.

Resume from worklog§0 and SKILL§5. Published baseline:
`a37194786ee69df36f35f42c2bf871be0c0341b2`. After final ZIP verification, commit and push
normally to the fixed branch, verify remote HEAD and give a pinned EPUB download.

**Final revised EPUB:** 14,660,034 bytes /414entries; SHA-256
`279f08b37c122c6e55cd2c00d4535194876791b1d84cd342546904a430306401`. Archive/tree parity414/414, CRC PASS,
315XML/312XHTML and2,190reference checks with zero structural errors. All96image/font
assets decoded. Chapters1–306 and every existing asset/style/reference/nav payload remain
unchanged. Old raw/upload bytes and worklog cycle history preserved. Inherited whole-book
editorial findings unchanged; both revised chapters pass their scoped gates.

**Everything below is the retained chapter-302 recovery baseline.** Statements that
chapter 303 is pending or that the original archive is unchanged describe recovery time,
not the current authorized production cycle. The original file's hash and payload inventory
remain recorded in the reports, even though the same root deliverable path is updated.

## 1. Recovery and preservation

The repository was already cloned into the Arena workspace. `git fetch origin main`
confirmed that both the imported commit and remote `main` were
`0cd94563452b8732976d907f186442471aa3a000` at recovery. No branch switch was needed.

Every member of the supplied EPUB was extracted to **`work_epub/`**, retaining its
internal path and exact bytes. Extraction rejected unsafe member paths and would not
overwrite a differing existing file. All 404 extracted files were subsequently compared
to the archive. No names, chapter text, images, fonts, or metadata were changed.

The original deliverable remains:

`Peninsula_Going_Viral_After_a_Dating_Scandal_with_Kim_Taeyeon_UC.epub`

| Baseline property | Verified value |
|---|---:|
| Archive bytes | 13,749,010 |
| Archive entries / extracted files | 404 / 404 |
| Chapters | 302, consecutive `ch001.xhtml`–`ch302.xhtml` |
| XHTML documents | 306: chapters plus cover, characters, glossary, navigation |
| XML documents including package/container/NCX | 309 |
| Manifest items | 401 |
| Spine entries | 306: 302 chapters plus four reference/navigation entries |
| NCX navPoints | 305 |
| Navigation list items, including landmarks | 308 |
| Images | 72: 71 JPEGs and one PNG |
| Embedded WOFF font faces | 20 |
| Stylesheets | 2 |
| Character-page cards / portrait references | 18 / 18 |
| Glossary cards | 61 |
| Highest `id-NN` identifier | `id-49`; next numeric image identifier is `id-50` |
| Tree-only / archive-only / changed payloads | 0 / 0 / 0 |

**SHA-256** — matches the chapter-302 ship prefix in the imported log:

```text
dcd310562b856ab31fc358e5d4e865635a4fef6711fa91a292d8379b553da494
```

The archive's first entry is the uncompressed, exact `application/epub+zip` mimetype.
CRC checking passes. All packaged resources are declared; none are missing from the
manifest. Chapter ordering agrees across the spine, NCX and the EPUB 3 contents nav.
The landmarks nav also links to chapter 1; it is not a duplicate contents entry.

## 2. Where everything lives

```text
Rumors_with_Taeyoen/
├── WORKSPACE_SETUP.md           Recovery findings and resume guide
├── AGENTS.md                    Short read-first handoff for future agents
├── SKILL.md                     Master production playbook
├── worklog.md                   Historical editorial state and cycle log
├── Peninsula_..._UC.epub        Unmodified chapter-302 deliverable
├── work_epub/
│   ├── mimetype
│   ├── META-INF/container.xml
│   └── OEBPS/
│       ├── content.opf
│       ├── toc.ncx
│       ├── text/               All 302 chapters and four reference/nav pages
│       ├── images/             All 72 original image payloads
│       ├── fonts/              All 20 original WOFF faces
│       └── styles/             fonts.css and stylesheet.css
├── raws/                       Untouched raws for chapters 299–303
├── uploads/                    Jessica_ref.jpg and Yoona_outfit_3.jpg
├── reports/                    Inventories, measured results and review candidates
├── workspace_audit.py          Repeatable, read-only recovery audit
├── validate_tree.py            Existing house structure/classes/text gate
├── punct_quotes.py             Existing quote audit; use dry run by default
├── repeat_check.py             Existing chapter repetition audit
├── audit_marks.py              Existing question-mark/phone-call audit
├── build_epub.py               Existing production packer; overwrites deliverable
├── .sl.json                    Reconstructed Stylelint core-rule config
├── package.json + lockfile     Original dependency declaration/lock, unchanged
└── requirements-audit.txt      Optional image/font decoding dependencies
```

The extracted tree is intentionally retained in workspace/Git changes for future editing.
Dependencies and scratch artifacts are ignored. The two supplied identity references and
all five raw files remain byte-identical to the repository import. Earlier raws were not
included; the historical log says routine raw retention began with chapter 299. Do not
invent or reverse-translate missing raw source files.

## 3. Scan results and their limits

The full tree was machine-scanned, including the complete text of every chapter. Skills,
cycle history, reference-page content and recent continuity were reviewed, with particular
attention to chapters 299–302 and all five available raws, including pending chapter 303.
Indexes cover about **697,128 English word tokens including chapter furniture**. This is
not a claim of a line-by-line human proofread of all 302 chapters, or certification of
perfect semantic continuity. The metrics tokenizer is stated in `workspace_audit.py`;
counts can differ slightly from previous cycle counts.

| Check | Recovery result |
|---|---|
| ZIP integrity and extracted payload parity | PASS |
| XML parse, manifest, spine, NCX and contents sequence | PASS |
| File links, CSS resource URLs and XML fragment targets | PASS; 2,142 reference checks, including repeat checks of manifest links |
| Existing `validate_tree.py` | PASS: 306 XHTML, zero undefined classes, unresolved file refs, straight double quotes or legacy CJK hits |
| Existing `punct_quotes.py` dry run | PASS: zero files flagged |
| Image/font decoding | PASS: 72 images and 20 WOFF faces decoded |
| Reconstructed 19-rule Stylelint configuration | PASS: both original stylesheets, no edits or autofix |
| Whole-book `audit_marks.py`, exact 302-chapter scope | FAIL under its hard-flag rules: 154 flags across 74 chapters; 453 soft candidates |
| Phone-call structure in that sweep | No hard structure flags |
| Whole-book `repeat_check.py` | REVIEW: 71 chapters flagged; quotations, exercises and repeated furniture need context |
| Repetition check for chapters 299–302 | Each has zero internal and zero previous-three-chapter 8-gram overlaps |
| `audit_marks.py` for chapters 299–302 | No hard flags; soft candidates are not a proof that every interrogative is correct |
| Packer smoke test | PASS: temporary output has the same 404 names and payloads as the import |

The temporary packer test used `.cache/packer-smoke.epub`, then deleted it. The production
EPUB was not overwritten. ZIP timestamps can change the archive hash even when all payloads
match, so the smoke-test hash is **not** a new ship hash.

### Inherited issues — recorded, not silently repaired

1. **Stale inventories and formulas.** The old documents say 68 images, 393 manifest items
   and 21 character portraits. Actual values are 72 images, 401 manifest items and 18
   portraits on the character page. There are also many in-chapter character images; these
   are different populations, not evidence of lost files. SKILL.md's next-image ID,
   NCX chapter offset, spine count and mimetype comparison instructions have been corrected
   to match the actual package. Historical ship entries are retained as history.
2. **Question punctuation.** The full chapter sweep finds 141 exact double-question-mark
   occurrences and 13 space-before-question-mark matches. Some spaced matches involve the
   permitted `???` fan-board register. The 453 `NO-QM?` lines are candidates, not 453 proven
   errors. Older deliberate flats and exercises are documented in the worklog; no mass
   replacement was applied. A manual spot-check also finds question-shaped flat endings in
   chapter 302 such as “Gorgeous, isn’t it.” and “Why do I keep coming to the roof.” These
   need explicit contextual triage, not an assumption that a clean detector equals proof.
3. **Reference-page damage/staleness.** `characters.xhtml` has incomplete joins in the
   Joo-hyun, Yoon-a and Ji-yeon bios (for example, a sentence ending in “while In Chapter
   301…”), Yoon-a events appended to Ji-ho's bio, and outdated acquisition/status rows.
   Ji-ho's “Some (with IU)” table entry conflicts with the Taeyeon-pairing decision in the
   cycle log and the chapter-85 discussion. Treat these as inherited editorial conflicts;
   consult the actual scene and logged decision before reusing a bio's claim.
4. **Name drift.** Recent chapters use `Kim Tae-yeon`, `Ham Eun-jung`, and `Hyo-min` in places
   where the playbook prefers `Kim Taeyeon`, `Hahm Eun-jung`, and `Park Hyomin`. These were
   not introduced by extraction. `reports/name_variants.tsv` locates measured usages.
   Do not extend those inconsistencies blindly or bulk-normalize older prose without review.
5. **Block conventions.** Six whisper blocks (chapters 266, 274, 295, 299, 300 and 302) have
   consecutive same-speaker lines and/or no final `wh-close`, contrary to the strict rule
   stated in SKILL.md. These are review candidates, not XML failures. A speaker may have
   several paragraphs; never invent an intervening reply just to satisfy alternation.
6. **Accessibility and metrics.** Chapter 283's `outfit_suit_Jiho.jpg` has an empty alt.
   The text sweep also records 72 doubled-word candidates and 272 chapters outside at least
   one current paragraph/dash target. Laughter, “had had,” lyrics and block text explain
   some flags. Chapter 282 remains the long pre-polish version described in the worklog;
   the historical statement that chapter 300 is the longest is not supported by the tree.
7. **Language-gate scope.** The glossary intentionally contains Korean Hangul. The legacy
   “CJK 0” result does not scan Hangul syllables, and it explicitly exempts fan Jamo.
   The supplemental scan found no Hangul syllables in the 302 chapter bodies. Preserve
   glossary terms and sanctioned fan emoticons; do not infer a global deletion mandate.
8. **Tool limitations.** `validate_tree.py` does not itself validate the manifest/spine/NCX
   or fragment IDs; the new recovery audit does. `audit_marks.py` needs real file paths:
   its advertised bare-filename example can return a misleading success on an unreadable
   file. `repeat_check.py`, conversely, expects bare chapter filenames as targets.
   Those legacy scripts were preserved; correct commands are below.

**Not performed:** EPUBCheck, visual proofs in EPUB reader engines, a full accessibility
conformance audit, per-glyph fallback/rendering verification, or a complete literary
re-edit. Font/image decoding and CSS lint do not establish reader rendering or likeness.

## 4. Continuity handoff

SKILL.md remains the rules source; the following are resume anchors, not replacement skills.
When documentation and prose disagree, verify the relevant scene and most recent explicit
editorial decision. Do not rewrite alternate-history fiction to match real-world biographies.

- **Protagonist:** Song Ji-ho, English name Sol, LA-born Korean-American; LOEN chairman.
  January 21, 1994 birth date and warm amber eyes. Height/stat values have developed over
  time; the old stat template is not a license to reset later growth.
- **Names/register:** Im Yoon-a; Bae Joo-hyun, nicknamed Cabbage; Chae Soo-bin; Lee Ji-eun;
  Park Ji-yeon. Preserve relational honorifics and action-beat dialogue attribution.
- **Romance:** Taeyeon is the official girlfriend. Yoon-a was promised an audition, not a
  guaranteed role; chapter 288's transactional offer was refused. Her chapter-295
  confession/kisses and chapter-296 promise to speak to Taeyeon are the continuation,
  not the raw's implication of an already consummated affair.
- **Corporate arc:** CCM takeover announced Friday September 27; Monday September 30 is
  the completed-acquisition market day. Kim Kwang-soo remains an embittered figure on the
  subsidiary floor in chapter 301, not someone to erase from the story because a fan
  comment says he is gone. T-ara's vindication campaign is planned, not already complete.
- **Rollout:** “7 Years” / “Stay with Me” released October 3; first stages October 5–6;
  America leg around October 10, with “Let Me Down Slowly” as the US lead single.
  The established album rollout includes October 15; do not restore conflicting raw dates.
- **Groups:** The most recent practice-room scenes explicitly have five trainees and
  five T-ara performers: ten women. Do not import the raw's eleven/six. This is a scene
  count, not permission to delete other established members from the whole novel.
- **SNSD schedule:** The earlier unnamed-tour convention was superseded in chapter 301:
  **Girls & Peace**, Singapore Indoor Stadium; “Mr.Mr.” fourth mini album moved to January
  2014, consuming Yoon-a's acting window. The main Taeyeon/Sica/Yoon-a conflict remains open.
- **Chapter 302 ending:** Thursday October 3, Ji-yeon and Joo-hyun duel; Joo-hyun reaches
  the roof and chooses not to hear the full relationship accounting. Debut promised for
  first half of 2014. Seung-wan witnesses the terrace kiss. Soo-bin offers Ji-yeon a guest
  slot at Ji-eun's late-November concerts. On **Friday October 4 at about 13:10 Singapore
  time**, Yoon-a collapses after concealing her cold through rehearsal.
- **Visual conventions:** Cardo 700 chapter titles, the cream EB Garamond italic pullquote
  card, left-aligned dossier `.dg-value`, `.self` on sent chat names. Existing styles are
  preserved exactly; `reports/style_usage.tsv` locates real markup examples for every
  chapter class, including blocks not fully enumerated in the playbook's short catalog.
- **Identity sources:** Jessica plates reset to `uploads/Jessica_ref.jpg`, not a chain of
  generated plates. Yoon-a uses `uploads/Yoona_outfit_3.jpg`. Keep previous user-supplied
  images and in-book placements intact. The latest Ji-yeon dress is goose-yellow, not the
  raw's later contradictory lilac.

### Chapter 303 is pending — recon only

`raws/ch303_raw.txt` exists (24,544 bytes). No `ch303.xhtml` exists in the book.
Its plot moves from the tense rehearsal room to news of Yoon-a's collapse, Ji-ho's flight
to Singapore, hospital room 308, a call to Jessica, Seohyun's departure for porridge, and
Yoon-a's question about whether he and his other partners can bear her love.

Before drafting:

- Resolve the **timeline**. Raw Seoul news at 10:30 is earlier than the established 13:10
  Singapore collapse (14:10 in Seoul). The raw's 17:00 Changi arrival and 6h55 flight cannot
  follow that event on the same-day schedule as written. Shift later timings coherently
  or propose another reconciliation; do not silently move chapter 302's collapse earlier.
- Keep the room at ten performers; carry the trainee knowledge/witness distinction forward.
- Normalize the raw protagonist name to Song Ji-ho, his eyes to established amber, Seoul
  and Singapore names to the house form, and Seo Ju-hyun/Seohyun to the existing usage.
- Preserve the raw verbatim in storage; drop site ads/OCR residue only from a future draft.
- The cold/exhaustion diagnosis, hospital choice, ward number, visit, romantic declarations
  and promised Jessica surprise are **pending raw beats**, not already published canon.
- Wire-up would use `ch303`, NCX `num_306` / playOrder `306`, and the next contents entry.
  With one chapter and no other resources, expected counts become 405 archive entries,
  402 manifest items, 307 spine entries, 306 NCX navPoints and 309 nav list items.
  Recompute if images or other resources are added. Preserve chapter 282's legitimate
  manifest alias `id-29`; do not rename it just because it is not `ch282`.

## 5. Commands for future work

Run from the repository root, not the historical parent directory:

```bash
cd /home/user/Rumors_with_Taeyoen
npm ci --ignore-scripts --no-audit --no-fund
python3 -m venv .venv
.venv/bin/pip install -r requirements-audit.txt

# Regenerates reports; never modifies the book or source archive.
.venv/bin/python workspace_audit.py --assets

# Existing house gates.
python3 validate_tree.py
python3 punct_quotes.py
python3 repeat_check.py ch302.xhtml
python3 audit_marks.py work_epub/OEBPS/text/ch302.xhtml
node_modules/.bin/stylelint --config .sl.json "work_epub/OEBPS/styles/*.css"
```

The recovery audit's exit code reflects structural/integrity checks; editorial findings
and legacy gate exit codes are recorded separately in its JSON. A zero recovery exit is
**not** “all editorial gates passed.” When drafting new chapters, tree/archive differences
are expected until packaging; this recovery-parity check is primarily for baseline and
post-build verification. Standard-library mode (`python3 workspace_audit.py`) omits asset
decoding. Recreate ignored dependencies when resuming if they are absent.

**Only after an authorized editorial cycle, all applicable gates and a worklog entry:**

```bash
python3 build_epub.py  # overwrites the production EPUB; do not use for inspection
```

Then verify the archive, record its new hash, refresh current-state documentation and
present the new EPUB as prescribed by SKILL.md. No production build or new ship occurred
in this setup cycle.

## 6. Audit artifacts

- `reports/workspace_audit.json` — authoritative machine-measured recovery summary.
- `reports/archive_inventory.tsv` — all 404 member paths, sizes, SHA-256 and compression.
- `reports/source_inventory.tsv` — raw/reference file hashes.
- `reports/chapter_index.tsv` — all chapter titles, date stamps and measured metrics.
- `reports/character_index.tsv`, `glossary_index.tsv` — reference-page indexes.
- `reports/style_usage.tsv` — each used chapter class and its chapter locations.
- `reports/name_variants.tsv` — selected continuity-sensitive spellings and occurrences.
- `reports/asset_validation.tsv` — all image dimensions and font decoding results.
- `reports/editorial_review.tsv` — heuristic candidates, not automatic repair instructions.
- `reports/validate_tree.txt`, `punct_quotes.txt`, `audit_marks.txt`, `repeat_check.txt`,
  `stylelint.txt`, `packer_smoke.txt` — raw gate evidence. Empty Stylelint output means no errors.

**Ready to resume:** the source tree, original book, raw archive, identity references,
production tools, recovered lint configuration, continuity handoff and review backlog are
in workspace storage. The next editorial task can start from this verified baseline.
