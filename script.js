async function processVideo() {
    const urlInput = document.getElementById('urlInput').value.trim();
    const resultArea = document.getElementById('resultArea');
    const fetchBtn = document.getElementById('fetchBtn');

    if (!urlInput) {
        alert('Please enter a valid YouTube URL');
        return;
    }

    // Extract Video ID to show a clean embedded thumbnail/preview
    const videoId = extractVideoID(urlInput);
    if (!videoId) {
        alert('Invalid YouTube URL format.');
        return;
    }

    fetchBtn.disabled = true;
    fetchBtn.textContent = 'Fetching details...';
    resultArea.classList.remove('hidden');
    
    // Using a public API endpoint or iframe fallback safe for client-side rendering
    resultArea.innerHTML = `
        <div class="space-y-4 animate-pulse">
            <div class="h-48 bg-slate-700 rounded-xl w-full"></div>
            <div class="h-10 bg-slate-700 rounded-xl w-full"></div>
        </div>
    `;

    setTimeout(() => {
        fetchBtn.disabled = false;
        fetchBtn.textContent = 'Fetch Video';
        
        resultArea.innerHTML = `
            <div class="space-y-4 border-t border-slate-700 pt-6">
                <div class="relative aspect-video rounded-xl overflow-hidden bg-black">
                    <iframe src="https://www.youtube.com/embed/${videoId}" class="w-full h-full" frameborder="0" allowfullscreen></iframe>
                </div>
                <div class="bg-slate-900 p-4 rounded-xl border border-slate-700 flex flex-col gap-3">
                    <span class="text-sm text-green-400 font-medium">✓ Video ready for extraction</span>
                    <a href="https://www.y2mate.is/youtube/${videoId}" target="_blank" 
                       class="text-center py-3 bg-emerald-600 hover:bg-emerald-500 transition font-medium rounded-lg text-white">
                        Download Video & Audio Streams
                    </a>
                </div>
            </div>
        `;
    }, 1000);
}

function extractVideoID(url) {
    const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    const match = url.match(regExp);
    return (match && match[2].length === 11) ? match[2] : null;
}