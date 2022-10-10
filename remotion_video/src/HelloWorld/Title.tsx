import { AbsoluteFill, Audio, Img, staticFile } from "remotion";
import React from 'react';
import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {FONT_FAMILY} from './constants';
import colorsJson from '../../public/uMzUL.json'

const title: React.CSSProperties = {
	fontFamily: FONT_FAMILY,
	fontWeight: 'bold',
	fontSize: 100,
	textAlign: 'center',
	position: 'absolute',
	top: 100,
	width: '100%',
};

const mainText: React.CSSProperties = {
	fontFamily: FONT_FAMILY,
	fontWeight: 'bold',
	fontSize: 100,
	textAlign: 'center',
	position: 'absolute',
	bottom: 160,
	width: '100%',
};

const word: React.CSSProperties = {
	marginLeft: 10,
	marginRight: 10,
	display: 'inline-block',
};

export const Title: React.FC<{
	titleText: string;
	titleColor: string;
	audioUrl?: string
}> = ({titleText = "Suara", titleColor, audioUrl = "uMzULsAVh7M.mp3"}) => {
	const videoConfig = useVideoConfig();
	const frame = useCurrentFrame();

	const {segments} = colorsJson;

	const renderSegment = () => {
		const secAdjustedFrame = frame / videoConfig.fps;
		const segmentIndex = segments.findIndex(segment => {
			return segment.start <= secAdjustedFrame && segment.end >= secAdjustedFrame;
		});
		const segment = segments[segmentIndex];
		if (!segment) {
			return <></>
		}
		const textDuration = segment.end - segment.start;
		const words = segment.text.split(" ");

		return (
			<div
				key={segment?.text}
			>
				{words.map((word, index) => {
					const wordStart = segment.start + (index * textDuration / words.length);
					return (
						<>
						<span 
							key={word}
							style={{
								color: titleColor,
								marginLeft: 10,
								marginRight: 10,
								opacity: (frame - (wordStart * videoConfig.fps)) / (videoConfig.fps * 0.5),
								transform: `scale(${spring({
									fps: videoConfig.fps,
									frame: frame - (wordStart * videoConfig.fps),
									config: {
										damping: 100,
										stiffness: 200,
										mass: 0.5,
									},
								})})`,
								display: 'inline-block',
							}}>
								{word}
							</span>
						</>
					)
				})}
			</div>
		);
	}

	const renderImage = () => {
		const images = ["img1.png", "img2.png"]
		const imageIndex = Math.floor(frame / (videoConfig.durationInFrames / images.length));
		const image = images[imageIndex];
		return (
			<Img src={staticFile(image)} style={{
				opacity: 0.25,
			}}/>
		);
	}

	return (
		<>
		{audioUrl ? <Audio src={staticFile(audioUrl)} /> : <></>}
		<AbsoluteFill>
			{renderImage()}
		</AbsoluteFill>
		<h1 style={title}>{titleText}</h1>
		<h1 style={mainText}>
			{renderSegment()}
			</h1>
		</>
	);
};
