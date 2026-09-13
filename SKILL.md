# SKILL.md — Peninsula Book Production Skills (V3 Pipeline)

**Purpose.** The single, deduplicated playbook for converting raw serialized chapters into the
publisher-grade English EPUB (*Peninsula: Going Viral After a Dating Scandal with Kim
Taeyeon*, Version 3). This file holds the **skills**; `worklog.md` holds the **state**
(cycle log, ships, canon pins). Do not duplicate skills between the two — SKILL.md is the
master reference, worklog §8 is the history.

**Current at ship:** 302 chapters · 404 entries · sha256 `dcd310562b856ab3…` · 20 embedded
faces · 68 images (manifest through id-49) · ncx 305 navPoints · nav 308 `<li>`.

**Operating skills (user directive, always on):** **DEEP SCAN** — read every raw line and
every produced line for content, contradictions, names, punctuation, and block contexts
before and after drafting; and **DEEP THINKING** — reason systematically about which style
block owns each context, resolve raw-internal contradictions, and fill thin context from
understanding rather than dropping it. Style-block maximalism is policy (§5).

**Update protocol — MANDATORY before every packaging:** refresh the *Current at ship* line
above, bump any learned rules into the relevant section (don't append duplicates), and add the
new ship's hash to worklog §8. SKILL.md is versioned by its *Current at ship* line only.

---

## 1 · Workspace map

| Path | Role |
|---|---|
| `/home/user/SKILL.md` | This playbook (skills) |
| `/home/user/worklog.md` | State: §0 read-first summary, §8 cycle log newest-first |
| `/home/user/work_epub/OEBPS/` | The book tree (`text/`, `images/`, `styles/`, `content.opf`, `toc.ncx`) |
| `/home/user/uploads/` | Reader-supplied identity sources of truth (rule #13) |
| `/home/user/validate_tree.py` | Gate: tree, manifests, refs, undefined classes, CJK |
| `/home/user/punct_quotes.py` | Gate: curly-quote integrity |
| `/home/user/repeat_check.py` | Gate: 8-gram repeats (arg = bare filename, run from `/home/user`) |
| `/home/user/audit_marks.py` | Gate: question marks + phone-call block structure |
| `/home/user/build_epub.py` | Packages the tree into the final EPUB |
| `/home/user/.sl.json` + `stylelint@16` | CSS lint (`npm i stylelint@16` per cycle — node_modules not persisted) |

---

## 2 · The per-chapter cycle (order of operations)

0. **Save the raw FIRST, before anything else** (user directive): the untouched chapter text
   goes to `/home/user/raws/chNNN_raw.txt` — verbatim, junk glyphs included — before any
   recon, drafting, or image work. The raws directory is the source archive.
1. **Recon.** Grep the tree for every named entity, callback, and block markup the raw
   touches (canon greps BEFORE writing). Sample the exact markup of any block to reuse.
2. **Draft** `work_epub/OEBPS/text/chNNN.xhtml` via a single `write_file`. Chapter skeleton:
   xml decl → head (fonts.css + stylesheet.css) → `page-wrapper` → `chapter-header`
   (chapter-number, chapter-title, chapter-rule) → `location-stamp` → body → close.
3. **Images** (if any): portrait/plate pipeline (§7). Center-crop 4:5, 1120×1400, JPEG q85
   optimize; install under `OEBPS/images/`; delete `gen/` and `image-search/` after.
4. **Wire-up** (§8 checklist), ET-parsing every touched file after each edit.
5. **Gates — ALL of §9, every touched chapter.** Fix and re-run until clean.
6. **Worklog §8 entry + §0 refresh** (before packaging — no build without a log entry).
7. **Build** (`python3 build_epub.py`) → in-archive asserts (§11) → update SKILL.md
   *Current at ship* → seal hash into worklog → `present_file`.

---

## 3 · Translation & voice standards

- **Language.** English publisher grade ("Version 3"). No machine-translation feel; no
  speaker names/tags before dialogue; attribution only via action beats.
- **Dialogue.** Natural, emotionally resonant, K-drama/light-novel register. Curly “ ” for
  all speech and quoted matter; straight quotes forbidden in prose. Em-dashes for cut-offs
  stay flush inside quotes ("I—").
- **Question marks.** Every true interrogative carries `?` — flattened questions are the #1
  AI-translation tell. Wh-clefts ("What gets through armor is…") and temporal clauses
  ("When I'm in Busan, you'll be here") are statements and keep periods; triage, don't
  blind-fix. Raw interrogatives (嗎 / ？？ / 吧？) restore their `?`. Incredulity is written `?!`, never
  `??`; runs of `???` are the sanctioned fan-board idiom (audit_marks exempts 3+, flags exactly-2).
- **Honorifics preserved:** eonni, oppa, unni (only where already canon), -ya/-ah, -nim;
  seonsaengnim; Hoejang-nim (172+ uses); romanized Korean sparingly and canon-spelled
  (ppalli, miane, saranghae, yeoboseyo, mwo/ya/aish/ne).
- **MC.** Song Ji-ho — Korean name order, Korean-American (LA-born), English name "Sol",
  chairman of LOEN. Never localize his name.
- **Names.** Real people under real romanizations (grep the tree first — the tree is the
  authority: Hahm Eun-jung, Park Hyomin, Qri, Lee Ah-reum…). OCs stay OCs. Normalize junk
   OCR variants (吳→Woo, 鹹→Hahm); do NOT change narrative to match real-world facts.
- **Chinese removal.** Zero hanzi/hangul-adjacent CJK in final text (gate-enforced). Drop
  junk ads, stray numerals, trailing glyph garbage. CN-net slang de-slanged: 霓虹→Japan,
  漢城→Seoul. Classical Chinese quotes → English paraphrase in an author-aside (describe,
  never print the hanzi). Author-vs-reader meta parentheses at chapter ends → dropped.
- **Tone.** Adults behaving like adults; intimacy non-graphic (suggest, then cut away).
  Sensitive content stays uncensored in outline but tasteful in rendering. No moralizing.
- **Freshness.** No recycled phrasings, sentence shapes, or imagery between chapters; vary
  paragraph rhythm; avoid LLM slop ("couldn't help but", "a testament to", etc.).

---

## 4 · Canon management

- **The tree is the canon.** Before importing any raw beat, grep for it. If the raw
  contradicts in-tree facts, **the tree wins** (e.g., 'Some' = his Taeyeon pairing, not an
  IU duet; '7 Years'/'Stay with Me' = Oct 3 single A/B-side). Log every re-cut in worklog §8.
- **Raw-internal contradictions** (Deep Scan): when the raw disagrees with itself (e.g.
  ch299's goose-yellow dress at the mirror but lilac at the gate), keep the version with the
  established setup and log the re-cut.
- **Timeline.** Maintain internal dates over raw stamps (ch293–297 run Thu Sep 26 → Sat
  Sep 28, 2013: cruise Thursday, notice + discharge Friday Sep 27, day 1,000 Saturday).
- **New characters:** full card on `characters.xhtml` (§8), portrait per §7.
- **Deliberate devices (do not re-litigate):** `???` fan-board idiom; ch277 "Are you sure.";
  honorific set per worklog §4; whisper-block alternation; one-sided chat threads vary
  receipt lines; author-aside label varied every chapter; SNSD tour left unnamed.
- **Trait/status labels** stay canonical: "Acquired — Trait:" em-dash form; stat-panel per
  ch094 (DOB Jan 21 1994, 182 cm, Charm keys).

---

## 5 · Style-block catalog (single source of truth)

Reuse before creating. **Style-block maximalism is policy (user directive): more blocks,
no compromising — even where the raw gives a context only a few lines thick, keep the block
and fill the remaining context from Deep Thinking understanding** (in-fiction, canon-safe).
Every block is labeled (its header/label line). Canonical class vocabularies — do not invent variants
without a §6 pass. All defined in `work_epub/OEBPS/styles/stylesheet.css` (section numbers
in brackets).

**Chapter furniture:** chapter-header (chapter-number · chapter-title · chapter-rule)
[Cardo 700 titles] · location-stamp (ls-date · ls-place · ls-sub) · scene-break ·
dialogue-line · thought · pullquote [16 — redesigned cream card, EB Garamond italic,
Cardo drop-quote, tri-color ribbon] · author-aside (aa-label · aa-text; **label text must
differ every chapter**).

**Game/system:** system-block (sys-*) · stat-panel · quest/award panels.

**Media & social:** app-screen (app-title · app-meta; notification cards) [13] ·
chat-container (chat-header · chat-name + .self on the SENDER only — the
owner of the window, whose bubbles are chat-sent and right-floated; every chat-sent bubble’s
name span MUST carry .self, never a plain chat-name (ch301 bug, fixed) · chat-bubble
chat-sent/chat-received · chat-meta · chat-clear) · phone-call [12: pc-head first child
(Courier slate), pc-me = this end, pc-them = far end, pc-note = stage direction;
**.sinister variant** = red-tinged bad calls; one-sided calls = pc-me only] ·
official-statement (os-masthead · os-meta · os-title · .os-note child for the attachment
footnote) [24] · official-post (op-band · op-handle · op-body · op-meta) · fanclub-block
(fc-header · fc-post>fc-user+fc-text · .mod/.founder) · trend-block (tr-*) ·
release-block (rs-*) · briefing-block (bf-band · bf-title · bf-item>bf-key · bf-note).

**Scene cards:** menu-block (mn-header · mn-sub · mn-course · mn-dish · mn-desc · mn-rule
· mn-note) · wardrobe-block (wd-header · wd-tag · wd-label · wd-effect · wd-note ·
wd-photo · wd-sub) · acting-block (ac-slate · ac-heading · ac-line · ac-cue) ·
lesson-block (lsn-header · lsn-term>lsn-gloss · lsn-step>lsn-count · lsn-note ·
lsn-teacher) · hand-note (hn-label; .reply variant) · memory-block (mb-label · mb-voice;
.bright variant) · whisper-block (wh-label · wh-voice · wh-reply · wh-note · wh-close;
strict voice/reply alternation, **wh-close last**).

**Characters page:** char-card > char-infobox (ci-name · ci-photo · ci-caption ·
ci-table) + char-bio; ci-table rows = Born/Group/Agency/In the story/…; caption line =
one-phrase epithet. New cards go before the closing char-note; the rights note covers all
portraits.

---

## 6 · New-block & font protocol

1. Grep the stylesheet for an existing block first (the §12 phone-call lesson: a new
   section was drafted for a block that already existed; the guard assert caught it).
2. If genuinely new: add a numbered CSS section with a header comment (context, class
   vocabulary, degrade behavior), child classes scoped under the parent selector, and a
   narrow-screen override beside the other media-query rules.
3. New font required → download the WOFF subset (fontsource/jsdelivr), verify glyph
   features with fontTools *before* committing (Cardo beat EB Garamond for titles because
   its default digits are lining — oldstyle figures turn "161" into "I6I"), add
   `@font-face` to fonts.css + `<item>` to the OPF manifest, and note the license (all
   faces SIL OFL). Unused faces stay embedded if they serve as fallbacks.
4. Re-run stylelint + validate_tree (undefined-class gate) after every CSS edit.

---

## 7 · Image pipelines

**Character portraits (real people).** Source a real photograph from the web
(image_search; prefer close-ups, portrait aspect). Install as
`images/char-{name}.jpg`, register id-NN in the OPF, add the char-card. Provenance noted
in worklog only, never printed in the book.

**Wardrobe plates (rule #12/#13).** Trigger: a *new* outfit with narrative intent (same
outoutfit twice = no plate). Identity source order: (1) reader upload in `uploads/` for
that person; (2) their canonical in-tree portrait/plate (rule #13 fallback); (3) AI
generation only for OCs without any source. Generate → center-crop 4:5 → 1120×1400 q85 →
`images/wd_{who}_{garment}.jpg` → manifest id → wd-photo embed. `generate_image` output is
unverifiable in-session — always tell the reader to check likeness; delete `gen/` and
`image-search/` after each round.

**Numbers.** Next manifest id = last + 1 (currently id-48). Record byte sizes in worklog.

---

## 8 · Wire-up checklist (per chapter)

1. `content.opf`: `<item id="chNNN" href="text/chNNN.xhtml">` before `</manifest>`;
   `<itemref idref="chNNN">` after the previous chapter; stamps
   "Volume One · Chapters 1–NNN" + "publisher's edition of Chapters 1–NNN"; any new image
   items.
2. `toc.ncx`: navPoint `num_{NNN+2}` / playOrder `{NNN+2}` after the previous chapter's
   block (navPoint count = chapters − nothing; currently 300 for 297).
3. `nav.xhtml`: `<li>` after the previous chapter (li count = chapters + 6).
4. `cover.xhtml` + `glossary.xhtml` footer stamps → NNN.
5. `characters.xhtml`: extend bios of touched characters (exact-anchor `str.replace`,
   never index math); new cards for new characters.
6. ET-parse every touched file, every edit.

---

## 9 · Pre-package gates (ALL mandatory, every touched chapter)

| Gate | Command (from `/home/user`) | Clean means |
|---|---|---|
| Tree/refs/classes | `python3 validate_tree.py` | PASS, zero undefined classes |
| Quote integrity | `python3 punct_quotes.py` | 0 files to rewrite |
| Repeats | `python3 repeat_check.py chNNN.xhtml` | 0 internal / 0 cross-chapter 8-grams; deliberate repeats (quotations, exercises) documented in worklog §8 — the tool's own caveat covers them once logged |
| **Question-mark audit** | `python3 audit_marks.py chNNN.xhtml` | No genuine NO-QM flags (triage wh-clefts); no `”?`/`??`/` ?`/`?”. ` malformations — **standing user directive** |
| **Phone-call audit** | in audit_marks.py | pc-head first child; body classes ⊆ pc-me/pc-them/pc-note — **standing user directive** |
| **Style-block deep scan** | re-read the finished chapter against §5 and the raw | every raw context owns its block; no context left in plain prose that the catalog covers — **standing user directive** |
| CSS lint | `npm i stylelint@16` then `node_modules/.bin/stylelint --config .sl.json "work_epub/OEBPS/styles/*.css"` | 0 errors |
| XML parse | ET.parse each touched file | no exception |
| CJK scan | in validate_tree/audit | 0 hanzi/hangul in final text |
| Doubled words | `\b(\w+) \1\b` scan | none (laughter ("ha ha") = false positive) |
| Metrics | inline calc | dashes ≤ ~5/1k · max paragraph ≤ ~100 words · “ ” parity equal |

---

## 10 · Metrics bands (house style)

Dash density ≤ ~5 per 1,000 words after surgery (keep speech cut-offs, canonical
"Acquired — Trait:" labels, and structural mn-/ac- dashes). Paragraphs: none over ~100
words (split monologues at seams; a one-line reaction beat is a valid splitter).
Punctuation: curly quotes balanced; ellipses for trailing thoughts; `?` on every
interrogative. Chapter length: whatever the raw needs — never truncate.

---

## 11 · Build, seal & verify

1. `python3 build_epub.py` → note entries/size/sha256.
2. In-archive asserts: mimetype first & STORED; `<item id="chNNN">` present; stamps
   correct; spine = chapters + 2; navPoint count; nav li; glossary footer; chapter content
   spot-strings; **byte-identical images** vs tree; phone-call/QM fixes present.
3. Tree↔archive symmetric diff must equal `{'mimetype'}` (the tree-side stray
   `work_epub/mimetype` is canonical and harmless — do NOT delete it).
4. Record the ship (entries, bytes, sha256 prefix) in worklog §8 + §0, and bump SKILL.md's
   *Current at ship* line. Then `present_file` the EPUB.

---

## 12 · Worklog discipline

- **§8 entry before build, always** (Source & scope · Canon held / re-cuts · Blocks ·
  Wire-up · Gates · Ship). Newest first. Multi-line anchors matched with
  whitespace-tolerant regex, not literal find.
- **§0 refresh** each cycle: chapter count, stamps, images, ship hash, and any new
  standing directives.
- Errors and dead ends get one line each in §8 or the errors note — future cycles must not
  relearn them.

---

## 13 · Known traps (do not relearn)

- Curly-vs-straight apostrophes break exact anchors — copy from file, not memory.
- Index-arithmetic inserts into characters.xhtml drift by one char; use exact-anchor
  `str.replace` (ch293's lost period; ch294+ clean).
- First-`</div>` extraction grabs the label's own div — parse with ElementTree instead.
- Multi-edit scripts: assert each anchor before writing; discard on mid-script failure
  (guards have caught a duplicate-block draft before it touched the sheet).
- Global `p{color}` beats inherited block color — scope child rules under the block.
- `repeat_check.py` takes a bare filename and runs from `/home/user`.
- `npm i stylelint@16` every cycle (node_modules not persisted).
- `OEBPS/`-prefixed paths inside in-archive asserts; tree paths unprefixed.
- A wardrobe block for a person with no identity source is skipped, not faked.
- One-sided phone calls: pc-me only, far end as pc-note murmurs (ch022 idiom).
- QM false positives: wh-clefts and temporal clauses are correct periods — triage, don't
  blind-fix.

---

## 14 · Update protocol (before every packaging)

1. Refresh the *Current at ship* header (chapters, entries, sha256, image id ceiling).
2. Fold any new rule from the closing cycle into its section above — merge, never append a
   duplicate. New traps → §13. New blocks/fonts → §5/§6. New gates → §9 table.
3. Keep this file the only place a *skill* lives; worklog §8 keeps only the *history*.
