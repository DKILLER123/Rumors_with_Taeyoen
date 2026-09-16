"""Read-only chapter/preservation gate; run from the repository root before packaging."""
from pathlib import Path
import collections
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('work_epub')
REPORTS = Path('reports/ch306')
X = '{http://www.w3.org/1999/xhtml}'
O = '{http://www.idpf.org/2007/opf}'
N = '{http://www.daisy.org/z3986/2005/ncx/}'
chapter = ROOT / 'OEBPS/text/ch306.xhtml'
r = ET.parse(chapter).getroot()
body = r.find(X + 'body')
text = ''.join(body.itertext())
words = lambda s: re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*", s)
classes = collections.Counter(c for e in body.iter() for c in e.get('class', '').split())
headers = {'memory-block':'mb-label', 'dossier-block':'dg-header', 'whisper-block':'wh-label',
           'hand-note':'hn-label', 'briefing-block':'bf-band', 'acting-block':'ac-slate',
           'menu-block':'mn-header', 'performance-block':'pf-header',
           'status-panel':'sp-header', 'lesson-block':'lsn-header',
           'system-block':'sys-header', 'contract-block':'ct-header', 'finance-block':'fb-header', 'app-screen':'app-title'}
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
for required in ['When the Gossip Hits Home', 'Seven thirteen.', 'About a hundred and eighty-five centimeters.',
                 'Kang Dong-won sunbaenim?', 'I’m sorry I hid it from you. Not that I’m with Yoon-a.',
                 'You… kissed her?', 'Hwang Mi-young! I said stay here!', 'Then he went after Taeyeon.']:
    assert required in text, required

raw = Path('raws/ch306_raw.txt')
raw_hash = hashlib.sha256(raw.read_bytes()).hexdigest()
assert raw_hash == '282c623d41f64996454688d78ed09d788495e3b7141a0e882d45081a6188f73b'
opf = ET.parse(ROOT / 'OEBPS/content.opf').getroot()
items = opf.findall(O + 'manifest/' + O + 'item')
spine = opf.findall(O + 'spine/' + O + 'itemref')
assert len(items) == 406 and len(spine) == 310
assert spine[-1].get('idref') == 'ch306'
assert sum(i.get('idref') == 'id-29' for i in spine) == 1
assert next(i for i in items if i.get('id') == 'id-29').get('href') == 'text/ch282.xhtml'
for item in items:
    assert (ROOT / 'OEBPS' / item.get('href')).is_file()
assert len(ET.parse(ROOT / 'OEBPS/toc.ncx').findall('.//' + N + 'navPoint')) == 309
assert len(ET.parse(ROOT / 'OEBPS/text/nav.xhtml').findall('.//' + X + 'li')) == 312
old = json.loads((REPORTS / 'baseline_payload_hashes.json').read_text())
now = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.rglob('*') if p.is_file()}
assert set(old) <= now.keys()
changed = sorted(k for k in old if old[k] != now[k])
added = sorted(now.keys() - old.keys())
assert changed == sorted(['OEBPS/content.opf', 'OEBPS/toc.ncx', 'OEBPS/text/nav.xhtml',
                          'OEBPS/text/cover.xhtml', 'OEBPS/text/glossary.xhtml', 'OEBPS/text/characters.xhtml'])
assert added == ['OEBPS/text/ch306.xhtml']
for n in range(1, 306):
    p = f'OEBPS/text/ch{n:03d}.xhtml'
    assert now[p] == old[p]
owners = []
for e in ET.parse(ROOT / 'OEBPS/text/characters.xhtml').iter():
    if e.get('class') == 'char-card':
        additions = [p for p in e.iter(X + 'p') if ''.join(p.itertext()).startswith(('In Chapter 306', 'At the end of Chapter 306'))]
        if additions:
            assert len(additions) == 1
            owners.append(next(''.join(c.itertext()) for c in e.iter() if c.get('class') == 'ci-name'))
assert sorted(owners) == sorted(['Song Ji-ho', 'Im Yoon-a', 'Kim Taeyeon', 'Tiffany (Hwang Mi-young)', 'Seohyun (Seo Ju-hyun)'])
census = {c: classes[c] for c in [*headers, 'pullquote'] if classes[c]}
assert sum(census.values()) == 51
metrics = {'result':'PASS', 'chapter':306, 'raw_sha256':raw_hash,
           'body_words_including_furniture':len(words(text)),
           'max_paragraph_words':max(len(words(''.join(p.itertext()))) for p in body.iter(X + 'p')),
           'em_dashes':text.count('—'), 'dashes_per_1000':round(text.count('—') * 1000 / len(words(text)), 3),
           'double_quote_parity':[text.count('“'), text.count('”')], 'question_marks':text.count('?'),
           'block_instances':sum(census.values()), 'block_types':len(census), 'block_census':census,
           'live_phone_calls':classes['phone-call'], 'chat_windows':classes['chat-container'],
           'images_added':0, 'bio_append_owners':owners, 'changed_baseline_payloads':changed,
           'added_payloads':added, 'unchanged_old_chapters':'305/305',
           'existing_assets_styles_preserved':True, 'chapter_sha256':now['OEBPS/text/ch306.xhtml']}
(REPORTS / 'prepackage.json').write_text(json.dumps(metrics, indent=2) + '\n')
questions = [' '.join(''.join(e.itertext()).split()) for e in body.iter()
             if e.tag in (X + 'p', X + 'span') and '?' in ''.join(e.itertext())
             and not any('?' in ''.join(c.itertext()) for c in e)]
(REPORTS / 'question_review.txt').write_text('\n\n'.join(questions) + '\n')
print(json.dumps(metrics, indent=2))
