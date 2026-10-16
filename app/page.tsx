// app/page.tsx
'use client';

import { useState } from 'react';

interface Format {
  itag: number;
  quality: string;
  container: string;
  url: string;
  contentLength: string;
}

interface VideoData {
  title: string;
  Author: string;
  durationSeconds: number;
  thumbnail: string;
  videoFormats: Format[];
  audioFormats: Format[];
}

export default function HomePage() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [videoData, setVideoData] = useState<VideoData | null>(null);

  const handleFetchInfo = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setVideoData(null);

    if (!url.trim()) {
      setError('Please enter a YouTube URL.');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('/api/info', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      setVideoData(data);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center p-6">
      <div className="max-w-2xl w-full mt-12">
        <h1 className="text-3xl font-bold text-center mb-2">
          YouTube Media Fetcher
        </h1>
        <p className="text-slate-400 text-center text-sm mb-8">
          Paste a link to your own or Creative Commons YouTube video to fetch stream links.
        </p>

        <form onSubmit={handleFetchInfo} className="flex gap-2 mb-6">
          <input
            type="url"
            placeholder="https://www.youtube.com/watch?v=..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1 rounded-lg bg-slate-900 border border-slate-700 px-4 py-3 text-sm focus:outline-none focus:border-red-500"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-red-600 hover:bg-red-500 disabled:opacity-50 px-6 py-3 rounded-lg font-medium text-sm transition"
          >
            {loading ? 'Fetching...' : 'Fetch Video'}
          </button>
        </form>

        {error && (
          <div className="p-4 mb-6 rounded-lg bg-red-950/60 border border-red-800 text-red-200 text-sm">
            {error}
          </div>
        )}

        {videoData && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-lg">
            <div className="md:flex">
              <img
                src={videoData.thumbnail}
                alt={videoData.title}
                className="w-full md:w-64 object-cover"
              />
              <div className="p-5 flex flex-col justify-between">
                <div>
                  <h2 className="font-semibold text-lg line-clamp-2">
                    {videoData.title}
                  </h2>
                  <p className="text-slate-400 text-sm mt-1">
                    Channel: {videoData.Author}
                  </p>
                </div>
                <span className="inline-block mt-3 text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded w-fit">
                  Duration: {formatDuration(videoData.durationSeconds)}
                </span>
              </div>
            </div>

            <div className="p-5 border-t border-slate-800 space-y-4">
              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
                  Video + Audio Streams
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {videoData.videoFormats.map((f) => (
                    <a
                      key={f.itag}
                      href={f.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      download
                      className="flex items-center justify-between bg-slate-800 hover:bg-slate-700 px-4 py-2.5 rounded-lg text-sm transition"
                    >
                      <span className="font-medium">
                        {f.quality} (.{f.container})
                      </span>
                      <span className="text-xs text-slate-400">
                        {f.contentLength}
                      </span>
                    </a>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">
                  Audio-Only Streams
                </h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {videoData.audioFormats.map((f) => (
                    <a
                      key={f.itag}
                      href={f.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      download
                      className="flex items-center justify-between bg-slate-800 hover:bg-slate-700 px-4 py-2.5 rounded-lg text-sm transition"
                    >
                      <span className="font-medium">
                        {f.quality} (.{f.container})
                      </span>
                      <span className="text-xs text-slate-400">
                        {f.contentLength}
                      </span>
                    </a>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}