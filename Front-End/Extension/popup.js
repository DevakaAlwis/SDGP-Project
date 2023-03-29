//check for current page is amazon product page or walmart product page to display the relevent div tags
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const currentTab = tabs[0];
  if (
    (currentTab.url.includes("amazon.com") &&
      currentTab.url.includes("/dp/")) ||
    (currentTab.url.includes("walmart.com") && currentTab.url.includes("/ip/"))
  ) {
    document.getElementById("main-container").style.display = "block";
  } else {
    document.getElementById("other-container").style.display = "block";
  }
});

// Get the product information from storage
chrome.storage.local.get(
    [
      "productName",
      "productId",
      "productImage",
      "productPrice",
      "productSiteName",
      "productRating",
      "productReviewCount",
      "productURL",
    ],
    function (result) {
        //get the elements from the popup.html
      const productImageEl = document.getElementById("product-image");
      const productNameEl = document.getElementById("product-name");
      const productIdEl = document.getElementById("product-id");
      const productPriceEl = document.getElementById("product-price");
      const productSiteNameEl = document.getElementById("product-site");
      const productRatingEl = document.getElementById("product-rating");
      const productReviewCountEl = document.getElementById("product-numberOfReviews");
      const productURLEl = document.getElementById("product-url");
  
      //put the data in the relavent positions
      imageURL = result.productImage;
      productImageEl.src = imageURL;
      productNameEl.innerText = result.productName;
      productIdEl.innerText = result.productId;
      productPriceEl.innerText = result.productPrice;
      productSiteNameEl.innerText = result.productSiteName;
      productRatingEl.innerText = result.productRating;
      productReviewCountEl.innerText = result.productReviewCount;
      productURLEl.href = result.productURL;
      productURLEl.textContent = result.productURL;
    }
  );
  
  