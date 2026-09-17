"""Independent ZIP seal; run from repo root after build and full-tree/assets audit."""
from pathlib import Path
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED

R = Path('reports/ch307')
TREE = Path('work_epub')
EPUB = Path('Peninsula_Going_Viral_After_a_Dating_Scandal_with_Kim_Taeyeon_UC.epub')
BASE = '060db570f945c2db7e6d7891374cc17940a38d56'
sha = lambda data: hashlib.sha256(data).hexdigest()
baseline = json.loads((R / 'baseline_payload_hashes.json').read_text())
pre = json.loads((R / 'prepackage.json').read_text())
audit = json.loads((R / 'full_tree/workspace_audit.json').read_text())
old_audit = json.loads(Path('reports/ch306/full_tree/workspace_audit.json').read_text())
current = {p.relative_to(TREE).as_posix(): sha(p.read_bytes()) for p in TREE.rglob('*') if p.is_file()}
with ZipFile(EPUB) as z:
    infos = z.infolist()
    assert len(infos) == len({i.filename for i in infos}) == 410
    assert infos[0].filename == 'mimetype' and infos[0].compress_type == ZIP_STORED
    assert z.read('mimetype') == b'application/epub+zip'
    assert all(i.compress_type == ZIP_DEFLATED for i in infos[1:])
    assert z.testzip() is None
    payload = {i.filename: sha(z.read(i)) for i in infos}
    assert payload == current
    for name in payload:
        assert not name.startswith('/') and '..' not in Path(name).parts
        if name.endswith(('.xml', '.xhtml', '.opf', '.ncx')):
            ET.fromstring(z.read(name))
    O = '{http://www.idpf.org/2007/opf}'
    X = '{http://www.w3.org/1999/xhtml}'
    N = '{http://www.daisy.org/z3986/2005/ncx/}'
    opf = ET.fromstring(z.read('OEBPS/content.opf'))
    manifest = opf.findall(O + 'manifest/' + O + 'item')
    spine = opf.findall(O + 'spine/' + O + 'itemref')
    items = {e.get('id'): e for e in manifest}
    assert len(items) == len(manifest) == 407
    assert len(spine) == 311 and spine[-1].get('idref') == 'ch307'
    assert all(s.get('idref') in items for s in spine)
    assert items['ch307'].get('href') == 'text/ch307.xhtml'
    assert all('OEBPS/' + i.get('href') in payload for i in manifest)
    assert items['id-29'].get('href') == 'text/ch282.xhtml'
    assert sum(s.get('idref') == 'id-29' for s in spine) == 1
    ncx = ET.fromstring(z.read('OEBPS/toc.ncx')).findall('.//' + N + 'navPoint')
    assert len(ncx) == 310 and ncx[-1].get('id') == 'num_310'
    assert ncx[-1].find(N + 'content').get('src') == 'text/ch307.xhtml'
    nav = ET.fromstring(z.read('OEBPS/text/nav.xhtml'))
    assert len(nav.findall('.//' + X + 'li')) == 313
    assert any(a.get('href') == 'ch307.xhtml' and 'How to Win Taeyeon’s Forgiveness' in ''.join(a.itertext()) for a in nav.iter(X+'a'))
    chapter = ET.fromstring(z.read('OEBPS/text/ch307.xhtml'))
    assert 'Neither piece has been eaten' in ''.join(chapter.itertext())
    assert payload['OEBPS/text/ch307.xhtml'] == pre['chapter_sha256']
    # Verify existing character content, not just four paragraph ownership labels.
    chars = ET.fromstring(z.read('OEBPS/text/characters.xhtml'))
    removed = 0
    for parent in chars.iter():
        for e in list(parent):
            if e.tag == X+'p' and ''.join(e.itertext()).startswith(('In Chapter 307', 'At the end of Chapter 307')):
                parent.remove(e)
                removed += 1
    old_chars = subprocess.check_output(['git', 'show', BASE + ':work_epub/OEBPS/text/characters.xhtml'])
    assert removed == 4
    assert ET.canonicalize(ET.tostring(chars), strip_text=True) == ET.canonicalize(ET.tostring(ET.fromstring(old_chars)), strip_text=True)
assert set(baseline) <= payload.keys()
changed = sorted(k for k in baseline if baseline[k] != payload[k])
added = sorted(payload.keys() - baseline.keys())
assert changed == pre['changed_baseline_payloads']
assert added == ['OEBPS/text/ch307.xhtml']
for n in range(1, 307):
    name = f'OEBPS/text/ch{n:03d}.xhtml'
    assert payload[name] == baseline[name]
for name in baseline:
    if name.startswith(('OEBPS/images/', 'OEBPS/fonts/', 'OEBPS/styles/')):
        assert payload[name] == baseline[name]
old_files = subprocess.check_output(['git', 'ls-tree', '-r', '-z', BASE, '--', 'raws', 'uploads'])
raw_upload_count = 0
for record in old_files.split(b'\0'):
    if not record:
        continue
    metadata, name = record.split(b'\t', 1)
    blob = metadata.split()[-1].decode()
    path = Path(name.decode())
    assert path.read_bytes() == subprocess.check_output(['git', 'cat-file', 'blob', blob]), str(path)
    raw_upload_count += 1
assert sha(Path('raws/ch307_raw.txt').read_bytes()) == pre['raw_sha256']
old_log = subprocess.check_output(['git', 'show', BASE + ':worklog.md']).decode()
new_log = Path('worklog.md').read_text()
marker = '### ch306 —'
assert old_log[old_log.index(marker):] == new_log[new_log.index(marker):]
assert audit['sha256'] == sha(EPUB.read_bytes())
assert audit['structural_errors'] == [] and audit['assets_decoded'] == 93
assert audit['editorial_review_counts'] == old_audit['editorial_review_counts']
assert audit['legacy_gate_exit_codes'] == old_audit['legacy_gate_exit_codes']
result = {
    'result': 'PASS', 'sha256': audit['sha256'], 'bytes': EPUB.stat().st_size,
    'archive_entries': 410, 'mimetype_first_stored': True, 'remaining_entries_deflated': True,
    'zip_crc': 'PASS', 'archive_tree_payload_parity': '410/410',
    'unchanged_old_chapters': '306/306', 'unchanged_existing_images_fonts_styles': True,
    'old_raws_and_uploads_unchanged': True, 'old_raw_upload_files_verified': raw_upload_count,
    'old_worklog_cycle_history_preserved': True, 'old_character_content_preserved': True,
    'raw307_sha256': pre['raw_sha256'], 'chapter307_sha256': pre['chapter_sha256'],
    'preserved_ch282_id29_alias': True, 'changed_baseline_payloads': changed, 'added_payloads': added,
    'manifest_items': 407, 'spine_items': 311, 'ncx_navpoints': 310, 'nav_li': 313,
    'decoded_images': 73, 'decoded_woff_faces': 20, 'reference_checks': audit['reference_checks'],
    'structural_errors': [], 'chapter_gate_status': 'PASS; four temporal-declarative/imperative flags triaged; phone and repeat checks passed',
    'legacy_book_wide_qm_repeat_flags': 'Existing book-wide findings retained; same exit codes and editorial category counts as 306; no new chapter repetition flags',
    'epubcheck': 'not performed', 'browser_layout_proof': '390px and 800px, with selected visual panel inspection'
}
(R / 'package_verification.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
