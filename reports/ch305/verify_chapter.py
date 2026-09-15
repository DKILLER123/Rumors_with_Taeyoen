"""Read-only chapter/preservation gate; run from the repository root before packaging."""
from pathlib import Path
import collections
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('work_epub')
REPORTS = Path('reports/ch305')
X = '{http://www.w3.org/1999/xhtml}'
O = '{http://www.idpf.org/2007/opf}'
N = '{http://www.daisy.org/z3986/2005/ncx/}'
chapter = ROOT / 'OEBPS/text/ch305.xhtml'
r = ET.parse(chapter).getroot()
body = r.find(X + 'body')
text = ''.join(body.itertext())
words = lambda s: re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*", s)
classes = collections.Counter(c for e in body.iter() for c in e.get('class', '').split())
headers = {'memory-block':'mb-label', 'dossier-block':'dg-header', 'whisper-block':'wh-label',
           'hand-note':'hn-label', 'briefing-block':'bf-band', 'acting-block':'ac-slate',
           'menu-block':'mn-header', 'performance-block':'pf-header',
           'status-panel':'sp-header', 'lesson-block':'lsn-header',
           'system-block':'sys-header', 'contract-block':'ct-header', 'finance-block':'fb-header'}
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
for required in ['Boyfriend Halo · LV3', 'Idol Aura · LV3', 'Dream Family Fund',
                 '37.8°C', 'prohibition on borrowed or third-party capital',
                 'not confirmation that she had already joined',
                 'best performance you can', 'I don’t want the massage anymore',
                 'Neither woman had entered', 'We’re doomed.']:
    assert required in text, required

raw = Path('raws/ch305_raw.txt')
raw_hash = hashlib.sha256(raw.read_bytes()).hexdigest()
assert raw_hash == 'da546059a30b46441b8671bb9dd6c47bb1cb5c908ca976d6e9c9dfbf4f49966d'
opf = ET.parse(ROOT / 'OEBPS/content.opf').getroot()
items = opf.findall(O + 'manifest/' + O + 'item')
spine = opf.findall(O + 'spine/' + O + 'itemref')
assert len(items) == 405 and len(spine) == 309
assert spine[-1].get('idref') == 'ch305'
assert sum(i.get('idref') == 'id-29' for i in spine) == 1
assert next(i for i in items if i.get('id') == 'id-29').get('href') == 'text/ch282.xhtml'
for item in items:
    assert (ROOT / 'OEBPS' / item.get('href')).is_file()
assert len(ET.parse(ROOT / 'OEBPS/toc.ncx').findall('.//' + N + 'navPoint')) == 308
assert len(ET.parse(ROOT / 'OEBPS/text/nav.xhtml').findall('.//' + X + 'li')) == 311
old = json.loads((REPORTS / 'baseline_payload_hashes.json').read_text())
now = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
assert set(old) <= now.keys()
changed = sorted(k for k in old if old[k] != now[k])
added = sorted(now.keys() - old.keys())
assert changed == sorted(['OEBPS/content.opf', 'OEBPS/toc.ncx', 'OEBPS/text/nav.xhtml',
                          'OEBPS/text/cover.xhtml', 'OEBPS/text/glossary.xhtml', 'OEBPS/text/characters.xhtml'])
assert added == ['OEBPS/text/ch305.xhtml']
for n in range(1, 305):
    p = f'OEBPS/text/ch{n:03d}.xhtml'
    assert now[p] == old[p]
owners = []
for e in ET.parse(ROOT / 'OEBPS/text/characters.xhtml').iter():
    if e.get('class') == 'char-card':
        additions = [p for p in e.iter(X + 'p') if ''.join(p.itertext()).startswith(('In Chapter 305', 'At the end of Chapter 305'))]
        if additions:
            assert len(additions) == 1
            owners.append(next(''.join(c.itertext()) for c in e.iter() if c.get('class') == 'ci-name'))
assert sorted(owners) == sorted(['Song Ji-ho', 'Im Yoon-a', 'Kim Taeyeon', 'Tiffany (Hwang Mi-young)'])
census = {c: classes[c] for c in [*headers, 'pullquote']}
assert sum(census.values()) == 53
metrics = {'result':'PASS', 'chapter':305, 'raw_sha256':raw_hash,
           'body_words_including_furniture':len(words(text)),
           'max_paragraph_words':max(len(words(''.join(p.itertext()))) for p in body.iter(X + 'p')),
           'em_dashes':text.count('—'), 'dashes_per_1000':round(text.count('—') * 1000 / len(words(text)), 3),
           'double_quote_parity':[text.count('“'), text.count('”')], 'question_marks':text.count('?'),
           'block_instances':sum(census.values()), 'block_types':len(census), 'block_census':census,
           'live_phone_calls':classes['phone-call'], 'chat_windows':classes['chat-container'],
           'images_added':0, 'bio_append_owners':owners, 'changed_baseline_payloads':changed,
           'added_payloads':added, 'unchanged_old_chapters':'304/304',
           'existing_assets_styles_preserved':True, 'chapter_sha256':now['OEBPS/text/ch305.xhtml']}
(REPORTS / 'prepackage.json').write_text(json.dumps(metrics, indent=2) + '\n')
questions = [' '.join(''.join(e.itertext()).split()) for e in body.iter()
             if e.tag in (X + 'p', X + 'span') and '?' in ''.join(e.itertext())
             and not any('?' in ''.join(c.itertext()) for c in e)]
(REPORTS / 'question_review.txt').write_text('\n\n'.join(questions) + '\n')
print(json.dumps(metrics, indent=2))
