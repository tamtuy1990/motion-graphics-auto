import React from 'react';
import {AbsoluteFill, Sequence, useCurrentFrame} from 'remotion';
type Box={x:number;y:number;w:number;h:number};
type Event={id:string;startFrame:number;endFrame:number;cueFrame:number;box:Box;template:string;props:any};
export type Board={version:string;canvas:{width:number;height:number;fpsNum:number;fpsDen:number;durationFrames:number};style:{fontFamily:string;locale:string;accent:string;foreground:string;background:string};events:Event[];protectedRegions:any[]};
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const Card=({e,b}:{e:Event;b:Board})=>{
 const f=useCurrentFrame(), duration=e.endFrame-e.startFrame, cue=e.cueFrame-e.startFrame;
 const fade=Math.min(clamp(f/6),clamp((duration-1-f)/6));
 const progress=clamp((f-cue)/Math.max(1,Math.min(24,duration-cue-8)));
 const eased=1-Math.pow(1-progress,3), p=e.props;
 const fmt=(v:number,d=0)=>v.toLocaleString(b.style.locale,{minimumFractionDigits:d,maximumFractionDigits:d});
 const size=Math.max(16,Math.min(40,b.canvas.width*e.box.w/13));
 let content:React.ReactNode;
 switch(e.template){
  case 'callout-v1': content=<><strong>{p.title}</strong><div style={{fontSize:size*.75,marginTop:10}}>{p.body}</div></>; break;
  case 'counter-v1': content=<><div>{p.label}</div><strong style={{fontSize:size*1.8}}>{fmt(p.from+(p.to-p.from)*eased,p.decimals)}</strong><span style={{marginLeft:12}}>{p.unit}</span></>; break;
  case 'bar-chart-v1': {const max=Math.max(1,...p.data.map((d:any)=>d.value));content=<><strong>{p.title} ({p.unit})</strong>{p.data.map((d:any,i:number)=><div key={i} style={{fontSize:size*.62,marginTop:8}}><div>{d.label}: {fmt(d.value,1)}</div><div style={{height:12,background:b.style.accent,width:`${100*d.value/max*eased}%`}}/></div>)}</>;break;}
  case 'infographic-v1': content=<><strong>{p.title}</strong>{p.items.map((d:any,i:number)=><div key={i} style={{opacity:clamp(progress* p.items.length-i+1),marginTop:12,fontSize:size*.8}}>{d.glyph} {d.label}</div>)}</>;break;
  case 'steps-v1': content=<><strong>{p.title}</strong>{p.steps.map((d:string,i:number)=><div key={i} style={{marginTop:12,fontSize:size*.8,color:progress>i/p.steps.length?b.style.accent:b.style.foreground}}>{i+1}. {d}</div>)}</>;break;
  default: throw new Error('Unsupported template: '+e.template);
 }
 return <div style={{position:'absolute',left:e.box.x*b.canvas.width,top:e.box.y*b.canvas.height,width:e.box.w*b.canvas.width,height:e.box.h*b.canvas.height,boxSizing:'border-box',padding:20,borderRadius:16,background:b.style.background,color:b.style.foreground,fontFamily:b.style.fontFamily,fontSize:size,lineHeight:1.25,opacity:fade,transform:`translateY(${(1-fade)*12}px)`,overflowWrap:'break-word'}}>{content}</div>;
};
export const Overlay=(b:Board)=><AbsoluteFill>{b.events.map(e=><Sequence key={e.id} from={e.startFrame} durationInFrames={e.endFrame-e.startFrame}><Card e={e} b={b}/></Sequence>)}</AbsoluteFill>;
