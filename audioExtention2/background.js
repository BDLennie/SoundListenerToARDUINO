let ws = null;
let lastState = null;

function connectWS() {
    if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
        return;
    }

    ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
    console.log("WebSocket verbonden");
    getAnyAudible().then(sendState);   // ← wacht op het resultaat, geeft een boolean door
    };
    ws.onclose = () => {
        console.log("WebSocket verbroken, opnieuw verbinden...");
        ws = null;
    };
    ws.onerror = (e) => {
        console.log("WebSocket fout:", e);
    };
}

function sendState(isPlaying) {
    if (isPlaying === lastState) return;   // niets veranderd, niets sturen
    lastState = isPlaying;
    console.log("State change:", isPlaying);

    connectWS();
    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ isPlaying }));
    }
}

// Kijkt over alle tabs of er érgens geluid speelt
function getAnyAudible() {
    return new Promise((resolve) => {
        chrome.tabs.query({ audible: true }, (tabs) => {
            resolve(tabs.length > 0);
        });
    });
}

// --- Het event: vuurt zodra een tab van audio-status wisselt ---
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.audible !== undefined) {
        getAnyAudible().then(sendState);
    }
});

// Ook reageren als een geluid-makende tab wordt gesloten
chrome.tabs.onRemoved.addListener(() => {
    getAnyAudible().then(sendState);
});

// --- Lifecycle: worker terugbrengen na slaap/herstart ---
chrome.runtime.onStartup.addListener(connectWS);
chrome.runtime.onInstalled.addListener(connectWS);

connectWS();