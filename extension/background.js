/* background.js */

// 1. Initialize User Identity on Install
browser.runtime.onInstalled.addListener(() => {
  // Generate a random ID for this user if one doesn't exist
  browser.storage.local.get("userId").then((result) => {
    if (!result.userId) {
      const newId = "user_" + Math.random().toString(36).substr(2, 9);
      browser.storage.local.set({ userId: newId });
      console.log("NeuroRead: Generated new Private User ID:", newId);
    }
  });

  // Create Context Menu Item
  browser.contextMenus.create({
    id: "neuro-analyze",
    title: "NeuroRead: Condense & Analyze Selection",
    contexts: ["selection"]
  });
});

// 2. Handle Context Menu Click
browser.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "neuro-analyze") {
    // Send message to the content script in the active tab
    browser.tabs.sendMessage(tab.id, {
      command: "analyzeSelection",
      text: info.selectionText
    });
  }
});
