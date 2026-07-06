let ws = null;
let audioCheckStarted = false;

function startAudioCheck() {
    if (audioCheckStarted) return;
    audioCheckStarted = true;

    console.log("Audio check gestart");

    setInterval(() => {
        chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
            if (!tabs || tabs.length === 0) return;

            const tab = tabs[0];
            const isPlaying = tab.audible === true;

            console.log("Tab geluid", isPlaying);

            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({isPlaying}));
            }
        });
    }, 100);
}

function connectWS() {
    ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
        console.log("WebSocket verbonden");
        startAudioCheck();
    }
    ws.onclose = () => {
        console.log("WebSocket verbroken, opnieuw verbinden...");
        audioCheckStarted = false;
        setTimeout(connectWS, 2000);
    };

    ws.onerror = (e) => {
        console.log("WebSocket fout:", e);
    };
}

connectWS();
