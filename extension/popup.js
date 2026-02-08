/* popup.js */

const statusDiv = document.getElementById("connectionStatus");
const urlInput = document.getElementById("backendUrl");

// 1. Load Saved URL
browser.storage.local.get(["backendUrl", "fontEnabled"]).then((res) => {
  if (res.backendUrl) {
    urlInput.value = res.backendUrl;
    checkConnection(res.backendUrl);
  }
  document.getElementById("fontToggle").checked = res.fontEnabled || false;
});

// 2. Save URL & Connect
document.getElementById("saveBtn").addEventListener("click", () => {
  const url = urlInput.value.replace(/\/$/, ""); // Remove trailing slash
  browser.storage.local.set({ backendUrl: url });
  checkConnection(url);
});

// 3. Test Connection
function checkConnection(url) {
  statusDiv.textContent = "Connecting...";
  fetch(`${url}/status`)
    .then(res => res.json())
    .then(data => {
      statusDiv.textContent = "✅ Connected: " + data.mode;
      statusDiv.style.color = "green";
    })
    .catch(err => {
      statusDiv.textContent = "❌ Connection Failed. Check URL & Visibility.";
      statusDiv.style.color = "red";
    });
}

// 4. Trigger Reader Mode
document.getElementById("readerModeBtn").addEventListener("click", () => {
  browser.storage.local.get("backendUrl").then((res) => {
    if(!res.backendUrl) return alert("Please connect backend first.");
    
    // Get current tab URL
    browser.tabs.query({active: true, currentWindow: true}).then((tabs) => {
      const currentUrl = tabs[0].url;
      // Fetch Reader View HTML
      fetch(`${res.backendUrl}/view/reader-mode`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentUrl })
      })
      .then(r => r.json())
      .then(data => {
        // Open in new tab (simplest robust way)
        const win = window.open("", "_blank");
        win.document.write(data.html);
      });
    });
  });
});

// 5. Toggle Font (Immediate)
document.getElementById("fontToggle").addEventListener("change", (e) => {
  const isChecked = e.target.checked;
  browser.storage.local.set({ fontEnabled: isChecked });
  
  // Send message to content script
  browser.tabs.query({active: true, currentWindow: true}).then((tabs) => {
    browser.tabs.sendMessage(tabs[0].id, {
      command: "toggleFont",
      enable: isChecked
    });
  });
});
