import argparse, json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def validate(t,s,m):
    for name,data in [('timing',t),('storyboard',s),('sentences',m)]:
        sch=load(ROOT/'schemas'/f'{name}.schema.json'); Draft202012Validator.check_schema(sch)
        Draft202012Validator(sch,format_checker=FormatChecker()).validate(data)
    def require(v,msg):
        if not v: raise ValueError(msg)
    def unique(items):
        ids=[x['id'] for x in items]; require(len(ids)==len(set(ids)), 'Duplicate ID'); return {x['id']:x for x in items}
    words=unique(t['words']); segments=unique(t['segments']); events=unique(s['events']); sentences=unique(m['sentences'])
    require([x['order'] for x in m['sentences']]==list(range(1,len(sentences)+1)), 'Sentence order not continuous')
    require(list(segments)==list(sentences), 'Sentence index differs from timing segments')
    previous=-1
    for w in t['words']:
        if w['status']=='unaligned': require(w['start'] is None and w['end'] is None,'Unaligned word has invented time'); continue
        require(w['start'] is not None and w['end'] is not None and w['start']<w['end'],'Invalid word time')
        require(w['start']>=previous,'Non-monotonic words'); previous=w['end']
    for seg in t['segments']:
        require(all(i in words for i in seg['wordIds']),'Unknown segment word')
        flags=[words[i]['status']=='aligned' for i in seg['wordIds']]
        state='aligned' if flags and all(flags) else 'partial' if any(flags) else 'unaligned'
        require(seg['status']==state,'Incorrect segment alignment status')
    c=s['canvas']; total=c['durationFrames']; fps=c['fpsNum']/c['fpsDen']
    require(c['width']%2==0 and c['height']%2==0,'MVP yuv420p requires even dimensions')
    for w in words.values():
        if w['status']=='aligned': require(w['end']<=total/fps+1/fps,'Word beyond video end')
    def bounds(b): require(b['x']+b['w']<=1.000001 and b['y']+b['h']<=1.000001,'Box outside canvas')
    def time_overlap(a,b): return max(a['startFrame'],b['startFrame'])<min(a['endFrame'],b['endFrame'])
    def box_overlap(a,b): return max(a['x'],b['x'])<min(a['x']+a['w'],b['x']+b['w']) and max(a['y'],b['y'])<min(a['y']+a['h'],b['y']+b['h'])
    for r in s['protectedRegions']:
        bounds(r['box']); require(0<=r['startFrame']<r['endFrame']<=total,'Invalid protected interval')
    for i,e in enumerate(s['events']):
        bounds(e['box']); require(0<=e['startFrame']<=e['cueFrame']<e['endFrame']<=total,'Invalid event interval')
        require(e['sentenceId'] in sentences,'Unknown sentence')
        require(all(w in words and words[w]['status']=='aligned' for w in e['evidenceWordIds']),'Invalid event evidence')
        require(set(e['evidenceWordIds'])<=set(sentences[e['sentenceId']]['wordIds']),'Evidence from another sentence')
        require(all(words[w]['confidence'] is not None and words[w]['confidence']>=.75 for w in e['evidenceWordIds']),'Evidence needs reviewed/calibrated confidence >= 0.75')
        if e['sourceKind']=='spoken':
            require(e['evidenceQuote'] in segments[e['sentenceId']]['originalText'],'Spoken quote absent')
            anchor=words[e['evidenceWordIds'][0]]['start']*fps
            require(abs(e['cueFrame']-anchor)<=2,'Cue exceeds 2 frame tolerance')
        for r in s['protectedRegions']: require(not(time_overlap(e,r) and box_overlap(e['box'],r['box'])),'Protected region collision')
        for other in s['events'][:i]: require(not time_overlap(e,other),'MVP permits one graphic at a time')
    for sentence in m['sentences']:
        seg=segments[sentence['id']]
        require(sentence['originalText']==seg['originalText'] and sentence['wordIds']==seg['wordIds'],'Sentence text/words changed')
        expected=[e['id'] for e in s['events'] if e['sentenceId']==sentence['id']]
        require(sentence['overlayEventIds']==expected,'Event association differs')
        a,b=sentence['startSeconds'],sentence['endSeconds']; require((a is None and b is None) or (a is not None and b is not None and a<b),'Invalid sentence time')
        aligned=[words[i] for i in sentence['wordIds'] if words[i]['status']=='aligned']
        if seg['status']=='aligned':
            require(a is not None and abs(a-aligned[0]['start'])<1e-6 and abs(b-aligned[-1]['end'])<1e-6,'Sentence boundaries differ from words')
        assets=sentence['assets']; unique(assets)
        require([x['assetOrder'] for x in assets]==list(range(1,len(assets)+1)), 'Asset order not continuous')
        for x in assets:
            if x['status']=='downloaded': require(x['rightsStatus']=='verified' and x['localPath'] and x['sha256'],'Downloaded asset missing rights/file hash')
            p,q=x['placementStartSeconds'],x['placementEndSeconds']
            require((p is None and q is None) or (p is not None and q is not None and p<q and a is not None and q<=b-a),'Invalid asset placement')
            if x['kind']=='video' and x['status']=='downloaded': require(x['sourceInSeconds'] is not None and x['sourceOutSeconds'] is not None and x['sourceInSeconds']<x['sourceOutSeconds'],'Invalid source trim')
    return {'status':'passed','events':len(events),'sentences':len(sentences),'scope':'schema and semantic checks; visual/audio QA still required'}
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('timing'); p.add_argument('storyboard'); p.add_argument('sentences'); a=p.parse_args()
    print(json.dumps(validate(load(a.timing),load(a.storyboard),load(a.sentences)),ensure_ascii=False))
