import { NextResponse } from 'next/server';
import ytdl from '@distube/ytdl-core';
import { Readable } from 'stream';

export const maxDuration = 60; // Set max duration for Vercel Serverless Function (seconds)

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const url = searchParams.get('url');
  const itag = searchParams.get('itag');

  if (!url || !ytdl.validateURL(url)) {
    return NextResponse.json({ error: 'Invalid YouTube URL' }, { status: 400 });
  }

  try {
    const info = await ytdl.getInfo(url);
    const format = ytdl.chooseFormat(info.formats, {
      quality: itag ? Number(itag) : 'highest',
    });

    // Sanitize title for safe filenames
    const cleanTitle = info.videoDetails.title.replace(/[^\w\s-]/gi, '').trim() || 'video';
    const extension = format.hasVideo ? format.container || 'mp4' : 'mp3';
    const contentType = format.mimeType || (format.hasVideo ? 'video/mp4' : 'audio/mpeg');

    const nodeStream = ytdl.downloadFromInfo(info, { format });
    const webStream = Readable.toWeb(nodeStream);

    const headers = new Headers({
      'Content-Disposition': `attachment; filename="${cleanTitle}.${extension}"`,
      'Content-Type': contentType,
    });

    if (format.contentLength) {
      headers.set('Content-Length', format.contentLength);
    }

    return new NextResponse(webStream, { headers });
  } catch (error) {
    return NextResponse.json({ error: 'Download stream failed' }, { status: 500 });
  }
}