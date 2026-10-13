import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {Overlay, Board} from './Overlay';
const defaults: Board = {version:'1.0',canvas:{width:1280,height:720,fpsNum:30,fpsDen:1,durationFrames:180},style:{fontFamily:'Arial',locale:'vi-VN',accent:'#60A5FA',foreground:'#FFFFFF',background:'#172033'},events:[],protectedRegions:[]};
const Root = () => <Composition id="Overlay" component={Overlay} width={1280} height={720} fps={30} durationInFrames={180} defaultProps={defaults} calculateMetadata={({props})=>({width:props.canvas.width,height:props.canvas.height,fps:props.canvas.fpsNum/props.canvas.fpsDen,durationInFrames:props.canvas.durationFrames})}/>;
registerRoot(Root);
