import { NextResponse } from 'next/server';
import ytdl from '@distube/ytdl-core';

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const url = searchParams.get('url');

  if (!url || !ytdl.validateURL(url)) {
    return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
  }

  try {
    const info = await ytdl.getInfo(url);
    
    // Filter formats that include both video and audio (or audio-only)
    const formats = info.formats
      .filter((f) => (f.hasVideo && f.hasAudio) || (!f.hasVideo && f.hasAudio))
      .map((f) => ({
        itag: f.itag,
        quality: f.qualityLabel || `${f.audioBitrate}kbps Audio`,
        container: f.container,
        hasVideo: f.hasVideo,
        hasAudio: f.hasAudio,
        contentLength: f.contentLength,
      }));

    return NextResponse.json({
      title: info.videoDetails.title,
      thumbnail: info.videoDetails.thumbnails.at(-1)?.url,
      duration: info.videoDetails.lengthSeconds,
      author: info.videoDetails.author.name,
      formats,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch video details. The video may be private or restricted.' },
      { status: 500 }
    );
  }
}