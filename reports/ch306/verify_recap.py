"""Confirm that the 305 overlap is confined to the explicitly replayed door exchange."""
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path.cwd()))
import repeat_check as house
p=Path('work_epub/OEBPS/text/ch306.xhtml');s=p.read_text()
anchor=s.index('The knock, revisited ·')
a=s.rfind('    <div class="acting-block">',0,anchor)
b=s.index('\n    </div>',anchor)+len('\n    </div>')
assert a>=0
scratch=Path('.cache/ch306_without_recap.xhtml');scratch.write_text(s[:a]+s[b:])
full=house.grams(house.words(str(p))); trimmed=house.grams(house.words(str(scratch)))
result={}
for n in (303,304,305):
 g=house.grams(house.words(f'work_epub/OEBPS/text/ch{n}.xhtml'))
 before=sorted(set(full)&set(g));after=sorted(set(trimmed)&set(g))
 assert not after,(n,after)
 result[str(n)]={'shared_8grams':len(before),'outside_explicit_recap':len(after),'matches':[' '.join(k) for k in before]}
assert result['305']['shared_8grams']==19
assert not any(v>1 for v in full.values())
Path('reports/ch306/recap_verification.json').write_text(json.dumps({'result':'PASS','internal_repeats':0,'scope':result},indent=2)+'\n')
print('PASS: 19 cross-chapter eight-grams, all in the intentional 305 door-dialogue replay; zero elsewhere.')
