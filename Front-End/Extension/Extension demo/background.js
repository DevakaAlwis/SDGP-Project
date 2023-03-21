chrome.action.setBadgeText({
  text: "-",
});

chrome.tabs.onUpdated.addListener(async (tab) => {
  if (tab.url && tab.url.includes("amazon.com/*")) {
    // We retrieve the action badge to check if the extension is 'ON' or 'OFF'
    const prevState = await chrome.action.getBadgeText({ tabId: tab.id });
    // Next state will always be the opposite
    const nextState = prevState === "4.2" ? "-" : "4.2";

    // Set the action badge to the next state
    await chrome.action.setBadgeText({
      tabId: tab.id,
      text: nextState,
    });
  }
});
