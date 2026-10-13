import argparse, hashlib, json, subprocess
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('video'); p.add_argument('output'); a=p.parse_args()
source=Path(a.video).resolve(); target=Path(a.output).resolve()
if source==target: raise SystemExit('Output must differ from source')
h=hashlib.sha256()
with source.open('rb') as f:
    for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(source)],text=True))
data['sourceSha256']=h.hexdigest(); data['sourcePath']=str(source)
target.write_text(json.dumps(data,indent=2),encoding='utf-8')
