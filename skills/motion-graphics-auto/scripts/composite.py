import argparse, json, re, subprocess
from pathlib import Path
from fractions import Fraction
from PIL import Image
def run(a): return subprocess.check_output(a,text=True)
def main():
    p=argparse.ArgumentParser(); p.add_argument('source'); p.add_argument('frames'); p.add_argument('storyboard'); p.add_argument('output'); p.add_argument('--execute',action='store_true'); a=p.parse_args()
    source=Path(a.source).resolve(); out=Path(a.output).resolve(); frames=Path(a.frames).resolve()
    if source==out or out.exists(): raise ValueError('Output must be a new file, never source')
    if out.suffix.lower()!='.mkv': raise ValueError('MVP compositor outputs MKV; add verified container adapter for MP4')
    s=json.loads(Path(a.storyboard).read_text(encoding='utf-8')); c=s['canvas']; rate=Fraction(c['fpsNum'],c['fpsDen'])
    info=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(source)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    if (v['width'],v['height'])!=(c['width'],c['height']): raise ValueError('Dimension mismatch')
    if Fraction(v['r_frame_rate'])!=rate or Fraction(v['avg_frame_rate'])!=rate: raise ValueError('MVP requires matching CFR')
    if int(v['nb_read_frames'])!=c['durationFrames']: raise ValueError('Frame count mismatch')
    if v.get('color_transfer') in ('smpte2084','arib-std-b67') or int(v.get('bits_per_raw_sample') or 8)>8: raise ValueError('HDR/high bit depth requires advanced compositor')
    if any(x.get('rotation',0) for x in v.get('side_data_list',[])) or float(v.get('tags',{}).get('rotate',0)): raise ValueError('Rotation requires advanced compositor')
    for stream in info['streams']:
        if stream['codec_type'] in ('video','audio') and abs(float(stream.get('start_time',0)))>.001: raise ValueError('Nonzero PTS requires advanced compositor')
    # Probe actual presentation timestamps; average/r_frame_rate alone cannot detect VFR.
    pts=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(source)]))['frames']
    times=[float(x['best_effort_timestamp_time']) for x in pts]
    tolerance=max(float(v['time_base'].split('/')[0])/float(v['time_base'].split('/')[1])*1.1,1e-5)
    if any(abs(t-i/float(rate))>tolerance for i,t in enumerate(times)): raise ValueError('VFR or irregular PTS detected')
    files=list(frames.glob('*.png'))
    def number(f):
        m=re.search(r'(\d+)$',f.stem)
        if not m: raise ValueError('PNG filename has no frame index')
        return int(m.group(1))
    files.sort(key=number)
    if len(files)!=c['durationFrames']: raise ValueError('Missing/extra PNG frames')
    indexes=[number(f) for f in files]
    if indexes!=list(range(indexes[0],indexes[0]+len(files))): raise ValueError('Noncontiguous frame sequence')
    for f in files:
        with Image.open(f) as im:
            if im.size!=(c['width'],c['height']) or im.mode!='RGBA': raise ValueError('Frames must be full-size RGBA')
    # ffconcat avoids depending on Remotion filename padding/start-number conventions.
    listing=frames/'overlay.ffconcat'
    lines=['ffconcat version 1.0']
    for f in files:
        if "'" in f.name: raise ValueError('Unsupported quote in frame name')
        lines.extend(["file '"+f.name+"'",'option framerate '+str(rate),'duration '+format(1/float(rate),'.12f')])
    graph='[0:v:0]setpts=PTS-STARTPTS[base];[1:v]setpts=PTS-STARTPTS[ov];[base][ov]overlay=eof_action=pass:repeatlast=0:shortest=0:format=auto,format=yuv420p[v]'
    cmd=['ffmpeg','-n','-i',str(source),'-f','concat','-safe','0','-i',str(listing),'-filter_complex',graph,'-map','[v]','-map','0:a?','-map_metadata','0','-c:v','libx264','-crf','18','-preset','medium','-fps_mode','passthrough','-c:a','copy',str(out)]
    if a.execute:
        if listing.exists(): raise ValueError('Existing overlay.ffconcat; use a fresh frames folder')
        listing.write_text('\n'.join(lines)+'\n',encoding='utf-8'); subprocess.run(cmd,check=True)
    else: print(json.dumps({'command':cmd,'note':'Dry run; concat manifest written only with --execute'},indent=2))
if __name__=='__main__': main()
