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

/* popup.js */

const statusDiv = document.getElementById("connectionStatus");
const urlInput = document.getElementById("backendUrl");
const userInput = document.getElementById("username");
const passInput = document.getElementById("password");

// 1. Load Saved Credentials
browser.storage.local.get(["backendUrl", "auth_user", "auth_pass", "fontEnabled"]).then((res) => {
  if (res.backendUrl) urlInput.value = res.backendUrl;
  if (res.auth_user) userInput.value = res.auth_user;
  if (res.auth_pass) passInput.value = res.auth_pass;
  
  if (res.fontEnabled) document.getElementById("fontToggle").checked = true;
});

// 2. Save & Test Connection
document.getElementById("saveBtn").addEventListener("click", () => {
  let url = urlInput.value.trim().replace(/\/$/, ""); // Strip trailing slash
  const user = userInput.value.trim();
  const pass = passInput.value.trim();

  browser.storage.local.set({ 
    backendUrl: url,
    auth_user: user,
    auth_pass: pass
  });

  checkConnection(url, user, pass);
});

function checkConnection(url, user, pass) {
  statusDiv.textContent = "Authenticating...";
  statusDiv.style.color = "#666";

  // We use the status endpoint, but strictly speaking status is public.
  // Let's try to hit a private endpoint to PROVE auth works.
  // We'll create a dummy request to reader-mode with empty data just to check auth headers.
  
  // Create Basic Auth Header
  const headers = new Headers();
  headers.set('Authorization', 'Basic ' + btoa(user + ":" + pass));
  headers.set('Content-Type', 'application/json');

  fetch(`${url}/dyslexia/v2/suggest`, {
    method: "POST",
    headers: headers,
    body: JSON.stringify({ sentence: "test", misspelled_word: "test" }) 
  })
  .then(response => {
    if (response.status === 401) throw new Error("Unauthorized");
    if (response.status !== 200) throw new Error("Server Error");
    return response.json();
  })
  .then(() => {
    statusDiv.textContent = "✅ Secure Connection Established";
    statusDiv.style.color = "green";
  })
  .catch(err => {
    if(err.message === "Unauthorized") {
      statusDiv.textContent = "❌ Invalid Password";
    } else {
      statusDiv.textContent = "❌ Connection Failed";
    }
    statusDiv.style.color = "red";
  });
}

// Font Toggle Logic
document.getElementById("fontToggle").addEventListener("change", (e) => {
  browser.storage.local.set({ fontEnabled: e.target.checked });
  browser.tabs.query({active: true, currentWindow: true}).then((tabs) => {
    browser.tabs.sendMessage(tabs[0].id, { command: "toggleFont", enable: e.target.checked });
  });
});
