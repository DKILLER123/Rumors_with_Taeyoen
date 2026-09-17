"""Run from repository root; add --package after the prelogged build."""
from pathlib import Path
import collections, hashlib, json, re, subprocess, sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

R=Path('reports/ch307_308_revision');TREE=Path('work_epub')
BASE='a37194786ee69df36f35f42c2bf871be0c0341b2'
BOOK=Path('Peninsula_Going_Viral_After_a_Dating_Scandal_with_Kim_Taeyeon_UC.epub')
X='{http://www.w3.org/1999/xhtml}';O='{http://www.idpf.org/2007/opf}';N='{http://www.daisy.org/z3986/2005/ncx/}'
sha=lambda data:hashlib.sha256(data).hexdigest()
words=lambda text:re.findall(r"[A-Za-z]+(?:[’'-][A-Za-z]+)*",text)
baseline=json.loads((R/'baseline_payload_hashes.json').read_text())
current={p.relative_to(TREE).as_posix():sha(p.read_bytes()) for p in TREE.rglob('*') if p.is_file()}
assert current.keys()==baseline.keys() and len(current)==414
changed=sorted(k for k in current if current[k]!=baseline[k])
assert changed==['OEBPS/content.opf','OEBPS/text/ch307.xhtml','OEBPS/text/ch308.xhtml']
assert all(current[f'OEBPS/text/ch{n:03d}.xhtml']==baseline[f'OEBPS/text/ch{n:03d}.xhtml'] for n in range(1,307))
# Only the package modification timestamp may differ outside the two rewritten chapters.
old_opf=subprocess.check_output(['git','show',BASE+':work_epub/OEBPS/content.opf']).decode()
new_opf=(TREE/'OEBPS/content.opf').read_text()
mask=lambda s:re.sub(r'(<meta property="dcterms:modified">).*?(</meta>)',r'\1TIMESTAMP\2',s)
assert mask(old_opf)==mask(new_opf)
raw_hashes={307:'6348de25e3b61e2fd85ddb0f2321c827e404abe428c08f71e630013b929dbfb6',308:'8e659fea6eb90498dd06a629c0ebe98c17aaf6f9ec041007aba26a4c0c5c02ef'}
metrics=[]
for n in [307,308]:
    assert sha(Path(f'raws/ch{n}_raw.txt').read_bytes())==raw_hashes[n]
    root=ET.parse(TREE/f'OEBPS/text/ch{n}.xhtml').getroot();body=root.find(X+'body')
    wrapper=next(e for e in body.iter() if e.get('class')=='page-wrapper')
    text=' '.join(body.itertext());classes=collections.Counter(c for e in body.iter() for c in e.get('class','').split())
    assert text.count('“')==text.count('”')
    assert not re.search(r'[\u3400-\u9fff\uac00-\ud7af\ufffd]',text)
    assert not re.search(r'\b([A-Za-z]+)\s+\1\b',text,re.I)
    assert not re.search(r'\?\?|\b(?:TODO|TBD|FIXME|placeholder)\b',text,re.I)
    assert '"' not in text and "'" not in text
    assert max(len(words(' '.join(p.itertext()))) for p in body.iter(X+'p'))<=100
    assert text.count('—')*1000/len(words(text))<=5
    panels=[e for e in wrapper if e.tag==X+'div' and e.get('class')!='location-stamp']
    census=collections.Counter(e.get('class') for e in panels)
    assert census==({ 'phone-call':1,'system-block':1} if n==307 else {'system-block':3,'dev-quest':1,'wardrobe-block':1})
    headers={'phone-call':'pc-head','system-block':'sys-header','dev-quest':'dq-header','wardrobe-block':'wd-header'}
    for e in panels:
        assert any(c.get('class')==headers[e.get('class')] and ''.join(c.itertext()).strip() for c in e.iter())
        # Numeric stats are substantive content too; this is a snapshot check, not a house quota.
        assert len(' '.join(e.itertext()).split())>=65
    plain=[e for e in wrapper if e.tag==X+'p' and e.get('class')!='scene-break']
    plain_words=sum(len(words(' '.join(e.itertext()))) for e in plain)
    panel_words=sum(len(words(' '.join(e.itertext()))) for e in panels)
    share=plain_words/(plain_words+panel_words)
    assert share>(.8 if n==307 else .6)
    if n==307:
        call=next(e for e in panels if e.get('class')=='phone-call')
        assert call[0].get('class')=='pc-head' and 'speakerphone' in call[0].text
        assert all(e.get('class') in ('pc-me','pc-them','pc-note') for e in list(call)[1:])
        for required in ['Papaya of Fuller Grace ×2','Permanent effect after consumption','In the car. Going back to the hotel.','I wrote ‘Some’ for Taeyeon nuna, but released it with Ji-eun.','When have I lied to you?','Height-Reforging Milk','Leeteuk oppa and Heechul oppa']:
            assert required in text,required
    else:
        assert classes['phone-call']==0 and classes['chat-container']==0
        assert len(list(body.iter(X+'img')))==2 and len(list(body.iter(X+'figure')))==1
        assert classes['dq-task']==classes['dq-gate']==4
        assert all(''.join(e.itertext())=='Not completed' for e in body.iter() if e.get('class')=='dq-gate')
        for required in ['May 30, 1990','age 23, or 24 by Korean age reckoning','168 cm / 47 kg','34A · 24 · 34','76',
        'Face 10 · Physique 8 · Voice 7 · Presence 9 · Experience 5 · Communication 8 · Confidence 7 · Learning 6 · Wealth 7 · Fame 9',
        'Vocal 58 · Dance 75 · Acting 60 · Composition 45','Born Idol','Forest Fawn','Swan Neck','Little Mischief',
        'Camera’s Darling','Pure Healing','Innate Poise','Contrasting Charm','35 years','Celebration Package ×1',
        'Acquired — Trait: Born Idol','Before Yoon-a turns 30','Best Actress','Acquired, not worn',
        'Baeksang Arts Awards','Blue Dragon Film Awards','Over-the-Shoulder Smile','A Scoundrel’s Special Touch',
        'twenty-five songs: twenty-two','three for the encore','fourteenth song','eighty-minute mark',
        'Eyes, Nose, Lips','Some','Into the New World']:
            assert required in text,required
    reading=[]
    for e in root.iter():
        if e.tag in (X+'p',X+'figcaption') or e.get('class') in ('sys-header','wd-header','dq-header','dq-task','pc-head'):
            line=' '.join(''.join(e.itertext()).split())
            if line:reading.append(line)
    (R/f'ch{n}_reading.txt').write_text('\n\n'.join(reading)+'\n')
    questions=[' '.join(''.join(e.itertext()).split()) for e in body.iter(X+'p') if '?' in ''.join(e.itertext())]
    (R/f'ch{n}_questions.txt').write_text('\n\n'.join(questions)+'\n')
    metrics.append({'chapter':n,'blocks_before':40 if n==307 else 44,'blocks_after':len(panels),'block_census':dict(census),
    'ordinary_paragraphs':len(plain),'ordinary_prose_words':plain_words,'panel_words':panel_words,'ordinary_prose_percent':round(share*100,1),
    'body_words_including_furniture':len(words(text)),'question_marks':text.count('?'),'quotes':[text.count('“'),text.count('”')],
    'em_dashes':text.count('—'),'max_paragraph_words':max(len(words(' '.join(p.itertext()))) for p in body.iter(X+'p')),
    'raw_sha256':raw_hashes[n],'chapter_sha256':current[f'OEBPS/text/ch{n}.xhtml']})
result={'result':'PASS','chapters':metrics,'changed_payloads':changed,'all_306_other_chapters_unchanged':True,
'all_assets_styles_reference_pages_navigation_unchanged':True,'payload_count':414,'added_or_removed_payloads':[]}
(R/'prepackage.json').write_text(json.dumps(result,indent=2)+'\n')
if '--package' in sys.argv:
    with ZipFile(BOOK) as z:
        infos=z.infolist();assert len(infos)==len({i.filename for i in infos})==414
        assert infos[0].filename=='mimetype' and infos[0].compress_type==ZIP_STORED
        assert z.read('mimetype')==b'application/epub+zip'
        assert all(i.compress_type==ZIP_DEFLATED for i in infos[1:]) and z.testzip() is None
        payload={i.filename:sha(z.read(i)) for i in infos};assert payload==current
        for name in payload:
            assert not name.startswith('/') and '..' not in Path(name).parts
            if name.endswith(('.xml','.xhtml','.opf','.ncx')):ET.fromstring(z.read(name))
        opf=ET.fromstring(z.read('OEBPS/content.opf'));manifest=opf.findall(O+'manifest/'+O+'item');spine=opf.findall(O+'spine/'+O+'itemref')
        assert len(manifest)==411 and len(spine)==312 and spine[-1].get('idref')=='ch308'
        assert len(ET.fromstring(z.read('OEBPS/toc.ncx')).findall('.//'+N+'navPoint'))==311
        assert len(ET.fromstring(z.read('OEBPS/text/nav.xhtml')).findall('.//'+X+'li'))==314
    for record in subprocess.check_output(['git','ls-tree','-rz',BASE,'--','raws','uploads']).split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1)
        assert Path(name.decode()).read_bytes()==subprocess.check_output(['git','cat-file','blob',meta.split()[-1].decode()])
    oldlog=subprocess.check_output(['git','show',BASE+':worklog.md']).decode();newlog=Path('worklog.md').read_text();marker='### ch308 — A Born Idol — September 17, 2026 — pre-build entry'
    assert oldlog[oldlog.index(marker):]==newlog[newlog.index(marker):]
    audit=json.loads((R/'full_tree/workspace_audit.json').read_text());oldaudit=json.loads(Path('reports/ch308/full_tree/workspace_audit.json').read_text())
    assert audit['sha256']==sha(BOOK.read_bytes()) and not audit['structural_errors']
    assert audit['assets_decoded']==96
    assert audit['editorial_review_counts']==oldaudit['editorial_review_counts']
    assert audit['legacy_gate_exit_codes']==oldaudit['legacy_gate_exit_codes']
    browser=json.loads((R/'browser_proof.json').read_text());assert len(browser)==4
    for b in browser:
        assert not b['errors'] and b['scrollWidth']<=b['width']
        assert all(i['loaded'] for i in b['images'])
        assert all(p['scrollWidth']<=p['clientWidth']+1 for p in b['panels'])
    result.update({'sha256':audit['sha256'],'bytes':BOOK.stat().st_size,'zip_crc':'PASS','archive_tree_parity':'414/414',
    'old_raws_uploads_history_preserved':True,'reference_checks':audit['reference_checks'],'assets_decoded':96,
    'inherited_editorial_findings_unchanged':True,'browser_widths':[390,800],'epubcheck':'not performed'})
    (R/'package_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
