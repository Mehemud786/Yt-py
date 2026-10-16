'use client';

import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [videoInfo, setVideoInfo] = useState(null);
  const [selectedItag, setSelectedItag] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFetchInfo = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setVideoInfo(null);

    try {
      const res = await fetch(`/api/info?url=${encodeURIComponent(url)}`);
      const data = await res.json();

      if (!res.ok) throw new Error(data.error || 'Could not fetch video');

      setVideoInfo(data);
      if (data.formats.length > 0) {
        setSelectedItag(data.formats[0].itag);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    if (!url || !selectedItag) return;
    window.location.href = `/api/download?url=${encodeURIComponent(url)}&itag=${selectedItag}`;
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-xl bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl">
        <h1 className="text-2xl font-bold mb-2 text-white">YouTube Video Downloader</h1>
        <p className="text-slate-400 text-sm mb-6">
          Paste a YouTube link below to inspect available streams and download.
        </p>

        <form onSubmit={handleFetchInfo} className="flex gap-3 mb-6">
          <input
            type="url"
            required
            placeholder="https://www.youtube.com/watch?v=..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-lg px-4 py-2.5 text-sm text-white focus:outline-none focus:border-red-500"
          />
          <button
            type="submit"
            disabled={loading}
            className="bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white font-medium px-5 py-2.5 rounded-lg text-sm transition"
          >
            {loading ? 'Fetching...' : 'Analyze'}
          </button>
        </form>

        {error && (
          <div className="p-4 mb-6 bg-red-950/50 border border-red-800 text-red-300 rounded-lg text-sm">
            {error}
          </div>
        )}

        {videoInfo && (
          <div className="bg-slate-800/60 border border-slate-700/80 rounded-xl p-4 flex flex-col gap-4">
            <div className="flex gap-4 items-center">
              {videoInfo.thumbnail && (
                <img
                  src={videoInfo.thumbnail}
                  alt={videoInfo.title}
                  className="w-32 h-20 object-cover rounded-lg"
                />
              )}
              <div className="flex-1 min-w-0">
                <h2 className="font-semibold text-white truncate">{videoInfo.title}</h2>
                <p className="text-xs text-slate-400 mt-1">{videoInfo.author}</p>
                <p className="text-xs text-slate-400">
                  Duration: {Math.floor(videoInfo.duration / 60)}m {videoInfo.duration % 60}s
                </p>
              </div>
            </div>

            <div className="flex gap-3 pt-2 border-t border-slate-700/80">
              <select
                value={selectedItag}
                onChange={(e) => setSelectedItag(e.target.value)}
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white"
              >
                {videoInfo.formats.map((f) => (
                  <option key={f.itag} value={f.itag}>
                    {f.hasVideo ? `Video (${f.quality})` : `Audio Only (${f.quality})`} - .{f.container}
                  </option>
                ))}
              </select>

              <button
                onClick={handleDownload}
                className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium px-5 py-2 rounded-lg text-sm transition"
              >
                Download
              </button>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}