chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg && typeof msg.isPlaying !== "undefined") {
        chrome.runtime.sendMessage({ isPlaying: msg.isPlaying });
    }
});
