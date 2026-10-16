// app/api/info/route.ts
import { NextRequest, NextResponse } from 'next/server';
import ytdl from '@distube/ytdl-core';

export async function POST(req: NextRequest) {
  try {
    const { url } = await req.json();

    if (!url || !ytdl.validateURL(url)) {
      return NextResponse.json(
        { error: 'Please provide a valid YouTube URL.' },
        { status: 400 }
      );
    }

    const info = await ytdl.getInfo(url);

    // Filter formats that contain both video and audio (typically MP4 up to 720p/1080p)
    const videoFormats = ytdl
      .filterFormats(info.formats, 'videoandaudio')
      .map((format) => ({
        itag: format.itag,
        quality: format.qualityLabel || 'Standard',
        container: format.container,
        url: format.url,
        contentLength: format.contentLength
          ? `${(parseInt(format.contentLength, 10) / (1024 * 1024)).toFixed(1)} MB`
          : 'Size unknown',
      }));

    // Filter audio-only formats
    const audioFormats = ytdl
      .filterFormats(info.formats, 'audioonly')
      .slice(0, 3)
      .map((format) => ({
        itag: format.itag,
        quality: `${format.audioBitrate || 128} kbps`,
        container: format.container,
        url: format.url,
        contentLength: format.contentLength
          ? `${(parseInt(format.contentLength, 10) / (1024 * 1024)).toFixed(1)} MB`
          : 'Size unknown',
      }));

    return NextResponse.json({
      title: info.videoDetails.title,
      Author: info.videoDetails.author.name,
      durationSeconds: parseInt(info.videoDetails.lengthSeconds, 10),
      thumbnail:
        info.videoDetails.thumbnails[info.videoDetails.thumbnails.length - 1]?.url || '',
      videoFormats,
      audioFormats,
    });
  } catch (error: any) {
    console.error('YTDL Error:', error);
    return NextResponse.json(
      { error: error.message || 'Failed to extract video details.' },
      { status: 500 }
    );
  }
}