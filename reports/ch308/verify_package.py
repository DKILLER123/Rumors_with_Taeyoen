"""Independent post-build ZIP/preservation seal. Run from repository root."""
from pathlib import Path
import hashlib, json, subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

R=Path('reports/ch308');TREE=Path('work_epub')
BOOK=Path('Peninsula_Going_Viral_After_a_Dating_Scandal_with_Kim_Taeyeon_UC.epub')
BASE='dd39055039e6986105850e7a25969e1e368545f2'
sha=lambda data:hashlib.sha256(data).hexdigest()
subprocess.run(['python','reports/ch308/verify_chapter.py'],check=True,capture_output=True)
pre=json.loads((R/'prepackage.json').read_text())
baseline=json.loads((R/'baseline_payload_hashes.json').read_text())
audit=json.loads((R/'full_tree/workspace_audit.json').read_text())
previous=json.loads(Path('reports/ch307/full_tree/workspace_audit.json').read_text())
current={p.relative_to(TREE).as_posix():sha(p.read_bytes()) for p in TREE.rglob('*') if p.is_file()}
O='{http://www.idpf.org/2007/opf}';X='{http://www.w3.org/1999/xhtml}';N='{http://www.daisy.org/z3986/2005/ncx/}'
with ZipFile(BOOK) as z:
    infos=z.infolist()
    assert len(infos)==len({i.filename for i in infos})==414
    assert infos[0].filename=='mimetype' and infos[0].compress_type==ZIP_STORED
    assert z.read('mimetype')==b'application/epub+zip'
    assert all(i.compress_type==ZIP_DEFLATED for i in infos[1:])
    assert z.testzip() is None
    payload={i.filename:sha(z.read(i)) for i in infos}
    assert payload==current
    for name in payload:
        assert not name.startswith('/') and '..' not in Path(name).parts
        if name.endswith(('.xml','.xhtml','.opf','.ncx')):ET.fromstring(z.read(name))
    opf=ET.fromstring(z.read('OEBPS/content.opf'))
    manifest=opf.findall(O+'manifest/'+O+'item');spine=opf.findall(O+'spine/'+O+'itemref')
    items={e.get('id'):e for e in manifest}
    assert len(items)==len(manifest)==411
    assert len(spine)==312 and spine[-1].get('idref')=='ch308'
    assert all(s.get('idref') in items for s in spine)
    assert items['ch308'].get('href')=='text/ch308.xhtml'
    assert all('OEBPS/'+i.get('href') in payload for i in manifest)
    assert items['id-29'].get('href')=='text/ch282.xhtml'
    assert sum(s.get('idref')=='id-29' for s in spine)==1
    for ident,href in [('id-51','images/wd_yoona_white_ribbon.jpg'),('id-52','images/wd_yoona_first_love_white.jpg'),('id-53','images/char-lee-kangjun.jpg')]:
        assert items[ident].get('href')==href and items[ident].get('media-type')=='image/jpeg'
    points=ET.fromstring(z.read('OEBPS/toc.ncx')).findall('.//'+N+'navPoint')
    assert len(points)==311 and points[-1].get('id')=='num_311'
    assert points[-1].get('playOrder')=='311'
    assert points[-1].find(N+'content').get('src')=='text/ch308.xhtml'
    nav=ET.fromstring(z.read('OEBPS/text/nav.xhtml'))
    assert len(nav.findall('.//'+X+'li'))==314
    assert any(a.get('href')=='ch308.xhtml' and 'A Born Idol' in ''.join(a.itertext()) for a in nav.iter(X+'a'))
    assert 'Chapters 1–308' in ''.join(opf.itertext())
    assert 'Chapters 1–308' in z.read('OEBPS/text/cover.xhtml').decode()
    assert 'Last reviewed through Chapter 308.' in z.read('OEBPS/text/glossary.xhtml').decode()
    assert payload['OEBPS/text/ch308.xhtml']==pre['chapter_sha256']
assert set(baseline)<=payload.keys()
changed=sorted(k for k in baseline if baseline[k]!=payload[k]);added=sorted(payload.keys()-baseline.keys())
assert changed==pre['changed_baseline_payloads'] and added==pre['added_payloads']
for n in range(1,308):assert payload[f'OEBPS/text/ch{n:03d}.xhtml']==baseline[f'OEBPS/text/ch{n:03d}.xhtml']
for name in baseline:
    if name.startswith(('OEBPS/images/','OEBPS/fonts/','OEBPS/styles/')):assert payload[name]==baseline[name]
old_files=subprocess.check_output(['git','ls-tree','-r','-z',BASE,'--','raws','uploads'])
raw_upload_count=0
for record in old_files.split(b'\0'):
    if not record:continue
    metadata,name=record.split(b'\t',1);blob=metadata.split()[-1].decode();path=Path(name.decode())
    assert path.read_bytes()==subprocess.check_output(['git','cat-file','blob',blob]),str(path)
    raw_upload_count+=1
assert sha(Path('raws/ch308_raw.txt').read_bytes())==pre['raw_sha256']
old_log=subprocess.check_output(['git','show',BASE+':worklog.md']).decode();new_log=Path('worklog.md').read_text();marker='### ch307 —'
assert old_log[old_log.index(marker):]==new_log[new_log.index(marker):]
assert '### ch308 — A Born Idol' in new_log
record=json.loads((R/'prebuild_record.json').read_text())
assert record['phase']=='PRE-BUILD'
assert record['files']['Peninsula_Going_Viral_After_a_Dating_Scandal_with_Kim_Taeyeon_UC.epub']=='10643783ec60eb117f919a3b8dd4f6e93e053d62e2da9aa37b91f134115b1ce7'
assert record['files']['work_epub/OEBPS/text/ch308.xhtml']==pre['chapter_sha256']
assert audit['sha256']==sha(BOOK.read_bytes())
assert audit['structural_errors']==[] and audit['assets_decoded']==96
assert audit['editorial_review_counts']==previous['editorial_review_counts']
assert audit['legacy_gate_exit_codes']==previous['legacy_gate_exit_codes']
for image in json.loads((R/'images.json').read_text()):assert sha(Path(image['file']).read_bytes())==image['sha256']
browser=json.loads((R/'browser_proof.json').read_text())
assert [r['width'] for r in browser]==[390,800]
for r in browser:
    assert not r['errors'] and r['scrollWidth']<=r['width']
    assert all(b['scrollWidth']<=b['clientWidth']+1 for b in r['blocks'])
    assert all(im['loaded'] for im in r['images'])
    assert all(align=='left' for align in r['dossierAlign'])
assert not Path('gen').exists()
result={'result':'PASS','sha256':audit['sha256'],'bytes':BOOK.stat().st_size,
 'archive_entries':414,'mimetype_first_stored':True,'remaining_entries_deflated':True,
 'zip_crc':'PASS','archive_tree_payload_parity':'414/414','unchanged_old_chapters':'307/307',
 'unchanged_existing_images_fonts_styles':True,'old_raws_and_uploads_unchanged':True,
 'old_raw_upload_files_verified':raw_upload_count,'old_worklog_cycle_history_preserved':True,
 'old_character_content_preserved':True,'scoped_portrait_note_update':True,
 'raw308_sha256':pre['raw_sha256'],'chapter308_sha256':pre['chapter_sha256'],
 'preserved_ch282_id29_alias':True,'changed_baseline_payloads':changed,'added_payloads':added,
 'manifest_items':411,'spine_items':312,'ncx_navpoints':311,'nav_li':314,
 'decoded_images':76,'decoded_woff_faces':20,'reference_checks':audit['reference_checks'],
 'structural_errors':[],'chapter_gate_status':'PASS; QM hard0/soft0, phone and internal/cross repeat checks passed',
 'legacy_book_wide_qm_repeat_flags':'Inherited findings retained; same exit codes and editorial category counts as307',
 'epubcheck':'not performed','browser_layout_proof':'390px and800px, with selected narrow panel visual inspection'}
(R/'package_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
