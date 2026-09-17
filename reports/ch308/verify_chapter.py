"""Read-only chapter/content/preservation gate. Run from the repository root."""
from pathlib import Path
import collections, hashlib, json, re, subprocess
import xml.etree.ElementTree as ET

ROOT = Path('work_epub')
R = Path('reports/ch308')
BASE = 'dd39055039e6986105850e7a25969e1e368545f2'
X = '{http://www.w3.org/1999/xhtml}'
O = '{http://www.idpf.org/2007/opf}'
N = '{http://www.daisy.org/z3986/2005/ncx/}'
sha = lambda data: hashlib.sha256(data).hexdigest()
body = ET.parse(ROOT / 'OEBPS/text/ch308.xhtml').find(X+'body')
text = ''.join(body.itertext())
words = lambda s: re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*", s)
classes = collections.Counter(c for e in body.iter() for c in e.get('class','').split())
headers = {'memory-block':'mb-label','dossier-block':'dg-header','whisper-block':'wh-label',
 'hand-note':'hn-label','briefing-block':'bf-band','acting-block':'ac-slate',
 'performance-block':'pf-header','status-panel':'sp-header','lesson-block':'lsn-header',
 'system-block':'sys-header','contract-block':'ct-header','app-screen':'app-title',
 'phone-call':'pc-head','wardrobe-block':'wd-header','dev-quest':'dq-header'}
for e in body.iter():
    cls = e.get('class','').split()
    for parent, header in headers.items():
        if parent in cls:
            assert any(header in child.get('class','').split() and ''.join(child.itertext()).strip() for child in e.iter()), parent
    if 'whisper-block' in cls:
        seq=[c.get('class') for c in e if c.get('class') in ('wh-voice','wh-reply')]
        assert seq[0]=='wh-voice' and seq[-1]=='wh-reply'
        assert all(a!=b for a,b in zip(seq,seq[1:]))
        assert e[-1].get('class')=='wh-close'
    if 'dev-quest' in cls:
        for required in ['dq-principle','dq-basis','dq-task','dq-num','dq-what','dq-gate','dq-reward']:
            assert any(required in c.get('class','').split() and ''.join(c.itertext()).strip() for c in e.iter()), required
    if 'wardrobe-block' in cls:
        assert len(list(e.iter(X+'img')))==1
assert text.count('“')==text.count('”')
assert not re.search(r'[\u3400-\u9fff\uac00-\ud7af\ufffd]',text)
assert not re.search(r'\b([A-Za-z]+)\s+\1\b',text,re.I)
assert not any(c in text for c in ['"', "'"])
assert not re.search(r'\?\?|\b(?:TODO|TBD|FIXME|placeholder)\b|\[\s*\]',text,re.I)
assert max(len(words(''.join(p.itertext()))) for p in body.iter(X+'p'))<=100
assert text.count('—')*1000/len(words(text))<=5
for required in ['May 30, 1990','23 · 24 by Korean age reckoning','168 cm · 47 kg','34A · 24 · 34',
 'Charm · component total','76','Born Idol','Forest Fawn','Swan Neck','Little Mischief',
 'Communication +1 · Affinity +1','Face +2','Expressiveness in film and television work +2',
 'Presence-related effects gain an additional +1','35 years','×1','Acquired — Trait:',
 'Before Yoon-a turns 30','Best Actress','First Love in White','Acquired, not equipped',
 'Baeksang Arts Awards','Blue Dragon Film Awards','Over-the-Shoulder Smile',
 'A Scoundrel’s Special Touch','fourteenth song','eighty-minute mark','Twenty-two songs',
 'Three more for the encore','Eyes, Nose, Lips','Some','Into the New World']:
    assert required in text,required
assert sum([10,8,7,9,5,8,7,6,7,9])==76
assert classes['dq-gate']==4
assert all(''.join(e.itertext())=='Not completed' for e in body.iter() if e.get('class')=='dq-gate')
phones=[e for e in body.iter() if e.get('class')=='phone-call']
assert len(phones)==1 and phones[0][0].get('class')=='pc-head'
assert all(e.get('class') in ('pc-me','pc-them','pc-note') for e in list(phones[0])[1:])
assert classes['pc-me']==3 and classes['pc-them']==0 and classes['chat-container']==0
assert 'Ji-ho’s side heard' in ''.join(phones[0][0].itertext())
rawhash=sha(Path('raws/ch308_raw.txt').read_bytes())
assert rawhash=='8e659fea6eb90498dd06a629c0ebe98c17aaf6f9ec041007aba26a4c0c5c02ef'
opf=ET.parse(ROOT/'OEBPS/content.opf').getroot()
items=opf.findall(O+'manifest/'+O+'item');spine=opf.findall(O+'spine/'+O+'itemref')
assert len(items)==411 and len(spine)==312 and spine[-1].get('idref')=='ch308'
assert len({e.get('id') for e in items})==411
assert sum(i.get('idref')=='id-29' for i in spine)==1
assert next(i for i in items if i.get('id')=='id-29').get('href')=='text/ch282.xhtml'
for item in items: assert (ROOT/'OEBPS'/item.get('href')).is_file()
assert len(ET.parse(ROOT/'OEBPS/toc.ncx').findall('.//'+N+'navPoint'))==311
assert len(ET.parse(ROOT/'OEBPS/text/nav.xhtml').findall('.//'+X+'li'))==314
old=json.loads((R/'baseline_payload_hashes.json').read_text())
now={p.relative_to(ROOT).as_posix():sha(p.read_bytes()) for p in ROOT.rglob('*') if p.is_file()}
assert set(old)<=now.keys()
changed=sorted(k for k in old if old[k]!=now[k]);added=sorted(now.keys()-old.keys())
assert changed==sorted(['OEBPS/content.opf','OEBPS/toc.ncx','OEBPS/text/nav.xhtml','OEBPS/text/cover.xhtml','OEBPS/text/glossary.xhtml','OEBPS/text/characters.xhtml'])
assert added==sorted(['OEBPS/text/ch308.xhtml','OEBPS/images/wd_yoona_white_ribbon.jpg','OEBPS/images/wd_yoona_first_love_white.jpg','OEBPS/images/char-lee-kangjun.jpg'])
for n in range(1,308): assert now[f'OEBPS/text/ch{n:03d}.xhtml']==old[f'OEBPS/text/ch{n:03d}.xhtml']
for name in old:
    if name.startswith(('OEBPS/images/','OEBPS/fonts/','OEBPS/styles/')): assert now[name]==old[name],name
chars=ET.parse(ROOT/'OEBPS/text/characters.xhtml').getroot()
cards=[e for e in chars.iter() if e.get('class')=='char-card'];assert len(cards)==19
owners=[]
for e in cards:
    additions=[p for p in e.iter(X+'p') if ''.join(p.itertext()).startswith('In Chapter 308')]
    if additions:
        assert len(additions)==1
        owners.append(next(''.join(c.itertext()) for c in e.iter() if c.get('class')=='ci-name'))
assert sorted(owners)==sorted(['Song Ji-ho','Im Yoon-a','Kim Taeyeon','Tiffany (Hwang Mi-young)','Jessica (Jung Soo-yeon)'])
# Remove only authorized additions, then compare all previously published character content.
removed=0;newcards=0
for parent in list(chars.iter()):
    for e in list(parent):
        if e.tag==X+'p' and ''.join(e.itertext()).startswith('In Chapter 308'):
            parent.remove(e);removed+=1
        elif e.get('class')=='char-card' and any(c.get('class')=='ci-name' and c.text=='Lee Kang-jun' for c in e.iter()):
            parent.remove(e);newcards+=1
        elif e.get('class')=='char-note':
            e.text=e.text.replace(' Lee Kang-jun, a fictional stage director, has an AI-generated illustrated portrait.','').replace('The remaining portraits are photographs of the real artists;','All other portraits are photographs of the real artists;')
old_chars=subprocess.check_output(['git','show',BASE+':work_epub/OEBPS/text/characters.xhtml'])
assert removed==5 and newcards==1
assert ET.canonicalize(ET.tostring(chars),strip_text=True)==ET.canonicalize(ET.tostring(ET.fromstring(old_chars)),strip_text=True)
census={c:classes[c] for c in headers if classes[c]}
assert sum(census.values())==44 and len(census)==15
result={'result':'PASS','chapter':308,'raw_sha256':rawhash,'body_words_including_furniture':len(words(text)),
 'max_paragraph_words':max(len(words(''.join(p.itertext()))) for p in body.iter(X+'p')),
 'em_dashes':text.count('—'),'dashes_per_1000':round(text.count('—')*1000/len(words(text)),3),
 'double_quote_parity':[text.count('“'),text.count('”')],'question_marks':text.count('?'),
 'block_instances':sum(census.values()),'block_types':len(census),'block_census':census,
 'live_phone_calls':1,'chat_windows':0,'pending_development_tasks':4,'images_added':3,
 'bio_append_owners':owners,'new_character':'Lee Kang-jun','old_character_content_preserved':True,
 'changed_baseline_payloads':changed,'added_payloads':added,'unchanged_old_chapters':'307/307',
 'existing_assets_styles_preserved':True,'chapter_sha256':now['OEBPS/text/ch308.xhtml']}
(R/'prepackage.json').write_text(json.dumps(result,indent=2)+'\n')
questions=[' '.join(''.join(e.itertext()).split()) for e in body.iter() if e.tag in (X+'p',X+'span') and '?' in ''.join(e.itertext()) and not any('?' in ''.join(c.itertext()) for c in e)]
(R/'question_review.txt').write_text('\n\n'.join(questions)+'\n')
print(json.dumps(result,indent=2))
