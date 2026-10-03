"""Shared offline data access; Python standard library only."""
import json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
STATS=('hp','str','mag','skl','spd','lck','def','res')
DIFFICULTIES=('Normal','Hard','Lunatic','Lunatic+')
MODES=('Classic','Casual')
SPOILERS=('No spoilers','Tactical spoilers','Full information')
def slug(s):
 s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
 s=s.replace('’',"'").replace('+',' plus ').replace("'",'')
 k=re.sub('[^a-z0-9]+','_',s.lower()).strip('_')
 return {'avatar':'robin','lonqu':'lon_qu','sayri':'say_ri','yenfay':'yen_fay'}.get(k,k)
def records(category):
 return json.loads((ROOT/'data'/category/(category+'.json')).read_text())['records']
def lookup(category,name):
 key=slug(name)
 for r in records(category):
  if r['id']==key or slug(r['name'])==key:return r
 raise ValueError(f'Unknown {category}: {name}')
def dump(value):print(json.dumps(value,indent=2,ensure_ascii=False))
def read_json(path):return json.loads(Path(path).read_text())
