/* content.js */

let BACKEND_URL = "";
let USER_ID = "";

// 1. Initialize Config
browser.storage.local.get(["backendUrl", "userId", "fontEnabled"]).then((res) => {
  BACKEND_URL = res.backendUrl;
  USER_ID = res.userId;
  if (res.fontEnabled) applyDyslexiaFont();
});

// 2. Listen for Messages (From Popup or Background)
browser.runtime.onMessage.addListener((msg) => {
  if (msg.command === "toggleFont") {
    if (msg.enable) applyDyslexiaFont();
    else removeDyslexiaFont();
  } 
  else if (msg.command === "analyzeSelection") {
    showCondensePanel(msg.text);
  }
});

// --- FEATURES ---

function applyDyslexiaFont() {
  document.body.style.fontFamily = "Arial, sans-serif";
  document.body.style.lineHeight = "1.6";
  document.body.style.letterSpacing = "0.05em";
  document.body.style.backgroundColor = "#FDFBF7"; // Cream tint
  document.body.style.color = "#333";
}

function removeDyslexiaFont() {
  document.body.style = ""; // Naive reset (reload recommended)
}

// 3. Double Click to Define/Correct
document.addEventListener("dblclick", async () => {
  if (!BACKEND_URL) return;

  const selection = window.getSelection().toString().trim();
  if (selection.length < 2) return;

  // We assume the user might want a definition OR a correction
  // For this demo, let's hit the "Suggest" endpoint to see if it's misspelled
  // Need to get the full sentence context? (Simplified for now)
  
  try {
    const response = await fetch(`${BACKEND_URL}/dyslexia/v2/suggest`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-User-ID": USER_ID // Private Learning!
      },
      body: JSON.stringify({
        sentence: document.body.innerText.substring(0, 500), // Naive context
        misspelled_word: selection
      })
    });
    
    const data = await response.json();
    showTooltip(data, selection);
  } catch (e) {
    console.error("Backend Error", e);
  }
});

function showTooltip(data, original) {
  // (Reuse the tooltip UI code from previous responses, 
  // but ensure it handles the 'suggestions' array from the backend)
  console.log("Suggestions:", data.suggestions);
  alert(`Dyslexic Suggestions for '${original}':\n` + 
    data.suggestions.map(s => `• ${s.word} (${s.confidence})`).join("\n")
  );
}

function showCondensePanel(text) {
  if (!BACKEND_URL) return alert("Connect Backend First");

  fetch(`${BACKEND_URL}/view/condense`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text })
  })
  .then(r => r.json())
  .then(data => {
    alert("Key Points:\n" + data.summary_bullets.join("\n"));
  });
}

/* content.js */

let CONFIG = {
  url: "",
  user: "",
  pass: ""
};

// 1. Initialize & Listen for Changes
function loadConfig() {
  browser.storage.local.get(["backendUrl", "auth_user", "auth_pass", "fontEnabled"]).then((res) => {
    CONFIG.url = res.backendUrl;
    CONFIG.user = res.auth_user;
    CONFIG.pass = res.auth_pass;
    
    if(res.fontEnabled) applyDyslexiaFont();
  });
}
loadConfig();

// Listen for updates from popup
browser.storage.onChanged.addListener(loadConfig);

// 2. Helper to make Authenticated Requests
async function secureFetch(endpoint, body) {
  if (!CONFIG.url || !CONFIG.user) return null;

  const authString = btoa(`${CONFIG.user}:${CONFIG.pass}`);
  
  const response = await fetch(`${CONFIG.url}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Basic ${authString}`
    },
    body: JSON.stringify(body)
  });

  if (response.status === 401) {
    console.error("Dyslexic: Authentication Failed. Check Extension Settings.");
    return null;
  }
  return response.json();
}

// 3. Double-Click Handler
document.addEventListener("dblclick", async () => {
  const selection = window.getSelection().toString().trim();
  if (selection.length < 2) return;

  const context = window.getSelection().anchorNode.parentElement.innerText.substring(0, 500);

  const data = await secureFetch("/dyslexia/v2/suggest", {
    sentence: context,
    misspelled_word: selection
  });

  if (data && data.suggestions && data.suggestions.length > 0) {
    showSuggestionBox(data, selection);
  }
});

// UI helper (Same as before, abbreviated)
function showSuggestionBox(data, original) {
  // ... existing popup UI code ...
  // When user clicks a suggestion, send FEEDBACK
  // Example button click:
  // secureFetch("/dyslexia/feedback", { 
  //   misspelling: original, 
  //   chosen: clickedWord, 
  //   action: "accepted" 
  // });
}

// ... Font Toggle Functions ...
