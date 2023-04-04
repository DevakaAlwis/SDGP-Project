const chrome = window.chrome;
// let currentUrl = "";
// let isAllowedSite = false;

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.type === 'PRODUCT_INFO') {
    // Save the product information to storage
    chrome.storage.local.set({
      productName: message.productName,
      productId: message.productId,
      productImage: message.productImage,
      productPrice: message.productPrice,
      productSiteName: message.productSiteName,
      productRating: message.productRating,
      productReviewCount: message.productReviewCount,
      productURL: message.productURL
    })

    // Show the extension popup
    chrome.action.setPopup({ popup: 'popup.html' })
  }
})
