"""Read-only chapter/preservation gate; run from the repository root before packaging."""
from pathlib import Path
import collections
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('work_epub')
REPORTS = Path('reports/ch307')
X = '{http://www.w3.org/1999/xhtml}'
O = '{http://www.idpf.org/2007/opf}'
N = '{http://www.daisy.org/z3986/2005/ncx/}'
chapter = ROOT / 'OEBPS/text/ch307.xhtml'
r = ET.parse(chapter).getroot()
body = r.find(X + 'body')
text = ''.join(body.itertext())
words = lambda s: re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*", s)
classes = collections.Counter(c for e in body.iter() for c in e.get('class', '').split())
headers = {'memory-block':'mb-label', 'dossier-block':'dg-header', 'whisper-block':'wh-label',
           'hand-note':'hn-label', 'briefing-block':'bf-band', 'acting-block':'ac-slate',
           'menu-block':'mn-header', 'performance-block':'pf-header',
           'status-panel':'sp-header', 'lesson-block':'lsn-header',
           'system-block':'sys-header', 'contract-block':'ct-header', 'finance-block':'fb-header', 'app-screen':'app-title', 'phone-call':'pc-head'}
for e in body.iter():
    cls = e.get('class', '').split()
    for parent, label in headers.items():
        if parent in cls:
            assert any(label in c.get('class', '').split() and ''.join(c.itertext()).strip() for c in e.iter()), parent
    if 'whisper-block' in cls:
        seq = [c.get('class') for c in e if c.get('class') in ('wh-voice', 'wh-reply')]
        assert seq[0] == 'wh-voice' and seq[-1] == 'wh-reply'
        assert all(a != b for a, b in zip(seq, seq[1:]))
        assert e[-1].get('class') == 'wh-close'
assert text.count('“') == text.count('”')
assert not re.search(r'[\u3400-\u9fff\uac00-\ud7af\ufffd]', text)
assert not re.search(r'\b([A-Za-z]+)\s+\1\b', text, re.I)
assert not any(c in text for c in ['"', "'"])
assert max(len(words(''.join(p.itertext()))) for p in body.iter(X + 'p')) <= 100
for required in ['How to Win Taeyeon’s Forgiveness', 'Papaya of Fuller Grace', '×2',
                 'Permanent effect after consumption', 'In the car. Going back to the hotel.',
                 'When have I lied to you?', 'no guest slot has been approved', 'Neither piece has been eaten']:
    assert required in text, required
phones=[e for e in body.iter() if e.get('class')=='phone-call']
assert len(phones)==1
assert phones[0][0].get('class')=='pc-head'
assert all(e.get('class') in ('pc-me','pc-them','pc-note') for e in list(phones[0])[1:])
assert 'speaker' in ''.join(phones[0][0].itertext())

raw = Path('raws/ch307_raw.txt')
raw_hash = hashlib.sha256(raw.read_bytes()).hexdigest()
assert raw_hash == '6348de25e3b61e2fd85ddb0f2321c827e404abe428c08f71e630013b929dbfb6'
opf = ET.parse(ROOT / 'OEBPS/content.opf').getroot()
items = opf.findall(O + 'manifest/' + O + 'item')
spine = opf.findall(O + 'spine/' + O + 'itemref')
assert len(items) == 407 and len(spine) == 311
assert spine[-1].get('idref') == 'ch307'
assert sum(i.get('idref') == 'id-29' for i in spine) == 1
assert next(i for i in items if i.get('id') == 'id-29').get('href') == 'text/ch282.xhtml'
for item in items:
    assert (ROOT / 'OEBPS' / item.get('href')).is_file()
assert len(ET.parse(ROOT / 'OEBPS/toc.ncx').findall('.//' + N + 'navPoint')) == 310
assert len(ET.parse(ROOT / 'OEBPS/text/nav.xhtml').findall('.//' + X + 'li')) == 313
old = json.loads((REPORTS / 'baseline_payload_hashes.json').read_text())
now = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
assert set(old) <= now.keys()
changed = sorted(k for k in old if old[k] != now[k])
added = sorted(now.keys() - old.keys())
assert changed == sorted(['OEBPS/content.opf', 'OEBPS/toc.ncx', 'OEBPS/text/nav.xhtml',
                          'OEBPS/text/cover.xhtml', 'OEBPS/text/glossary.xhtml', 'OEBPS/text/characters.xhtml'])
assert added == ['OEBPS/text/ch307.xhtml']
for n in range(1, 307):
    p = f'OEBPS/text/ch{n:03d}.xhtml'
    assert now[p] == old[p]
owners = []
for e in ET.parse(ROOT / 'OEBPS/text/characters.xhtml').iter():
    if e.get('class') == 'char-card':
        additions = [p for p in e.iter(X + 'p') if ''.join(p.itertext()).startswith(('In Chapter 307', 'At the end of Chapter 307'))]
        if additions:
            assert len(additions) == 1
            owners.append(next(''.join(c.itertext()) for c in e.iter() if c.get('class') == 'ci-name'))
assert sorted(owners) == sorted(['Song Ji-ho', 'Im Yoon-a', 'Kim Taeyeon', 'Tiffany (Hwang Mi-young)'])
census = {c: classes[c] for c in [*headers, 'pullquote'] if classes[c]}
assert sum(census.values()) == 40
metrics = {'result':'PASS', 'chapter':307, 'raw_sha256':raw_hash,
           'body_words_including_furniture':len(words(text)),
           'max_paragraph_words':max(len(words(''.join(p.itertext()))) for p in body.iter(X + 'p')),
           'em_dashes':text.count('—'), 'dashes_per_1000':round(text.count('—') * 1000 / len(words(text)), 3),
           'double_quote_parity':[text.count('“'), text.count('”')], 'question_marks':text.count('?'),
           'block_instances':sum(census.values()), 'block_types':len(census), 'block_census':census,
           'live_phone_calls':classes['phone-call'], 'chat_windows':classes['chat-container'],
           'images_added':0, 'bio_append_owners':owners, 'changed_baseline_payloads':changed,
           'added_payloads':added, 'unchanged_old_chapters':'306/306',
           'existing_assets_styles_preserved':True, 'chapter_sha256':now['OEBPS/text/ch307.xhtml']}
(REPORTS / 'prepackage.json').write_text(json.dumps(metrics, indent=2) + '\n')
questions = [' '.join(''.join(e.itertext()).split()) for e in body.iter()
             if e.tag in (X + 'p', X + 'span') and '?' in ''.join(e.itertext())
             and not any('?' in ''.join(c.itertext()) for c in e)]
(REPORTS / 'question_review.txt').write_text('\n\n'.join(questions) + '\n')
print(json.dumps(metrics, indent=2))
