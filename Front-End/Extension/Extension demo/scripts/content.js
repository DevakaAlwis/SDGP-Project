// Check if the current page is an Amazon or walmart product page
if (isAmazonProductPage() || isWalmartProductPage()) {
  const productName = getProductName();
  const productId = getProductId();
  const productImage = getProductImage();
  const productPrice = getProductPrice();
  const productSiteName = getProductSiteName();
  const productRating = getProductRating();
  const productReviewCount = getProductReviewCount();
  const productURL = getProductURL();
  console.log(
    productName,
    productId,
    productImage,
    productPrice,
    productSiteName,
    productRating,
    productReviewCount,
    productURL
  );
  // Display the product information in the extension popup
  chrome.runtime.sendMessage({
    type: "PRODUCT_INFO",
    productId: productId,
    productName: productName,
    productImage: productImage,
    productPrice: productPrice,
    productSiteName: productSiteName,
    productRating: productRating,
    productReviewCount: productReviewCount,
    productURL: productURL,
  });
}

// Function to check if the current page is an Amazon product page
function isAmazonProductPage() {
  return (
    window.location.hostname.includes("amazon.com") &&
    window.location.pathname.includes("/dp/")
  );
}

// Function to check if the current page is an walmart product page
function isWalmartProductPage() {
  return (
    window.location.hostname.includes("walmart.com") &&
    window.location.pathname.includes("/ip/")
  );
}

// Function to get the product name from the page
function getProductName() {
  let productName = "";
  if (isAmazonProductPage()) {
    productName = document.getElementById("productTitle").innerText.trim();
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    productName =
      data.props.pageProps.initialData.data.contentLayout.pageMetadata
        .pageContext.itemContext.name;
  }
  return productName;
}

// Function to get the product ID from the page
function getProductId() {
  let productId = "";
  if (isAmazonProductPage()) {
    const asinRegex = /dp\/(\w{10})/;
    const matches = asinRegex.exec(window.location.href);
    productId = matches[1];
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    productId =
      data.props.pageProps.initialData.data.contentLayout.pageMetadata
        .pageContext.itemContext.itemId;
  }
  return productId;
}

// Function to get the product Image Link from the page
function getProductImage() {
  let productImage = "";
  if (isAmazonProductPage()) {
    productImage = document
      .getElementById("imgTagWrapperId")
      .getElementsByTagName("img")[0].src;
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    productImage =
      data.props.pageProps.initialData.data.product.imageInfo.allImages[0].url;
  }
  return productImage;
}

// Function to get the product Price from the page
function getProductPrice() {
  let productPrice = "";
  if (isAmazonProductPage()) {
    const priceElement = document.getElementsByClassName(
      "reinventPricePriceToPayMargin"
    )[0];
    productPrice = priceElement.querySelector(".a-offscreen").innerText.trim();
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    productPrice =
      data.props.pageProps.initialData.data.product.priceInfo.currentPrice
        .price;
  }
  return productPrice;
}

// Function to get the product Site Name from the page
function getProductSiteName() {
  let productSiteName = "";
  if (isAmazonProductPage()) {
    if (window.location.hostname.includes("amazon.com")) {
      productSiteName = "Amazon";
    }
  } else if (isWalmartProductPage()) {
    productSiteName = "Walmart";
  }
  return productSiteName;
}

// Function to get the product Rating from the page
function getProductRating() {
  let productRating = "";
  if (isAmazonProductPage()) {
    const titleElement = document.querySelector("#acrPopover");
    productRating = titleElement.getAttribute("title");
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    productRating =
      data.props.pageProps.initialData.data.reviews.averageOverallRating;
  }
  return productRating;
}

// Function to get the product Review Count from the page
function getProductReviewCount() {
  let reviewCount = "";
  if (isAmazonProductPage()) {
    const productReviewCount = document
      .getElementById("acrCustomerReviewText")
      .innerText.trim();
    const ratingWithoutComma = productReviewCount.replace(",", "");
    reviewCount = parseInt(ratingWithoutComma);
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    reviewCount =
      data.props.pageProps.initialData.data.reviews.totalReviewCount;
  }
  return reviewCount;
}

// Function to get the product URL from the page
function getProductURL() {
  let productURL = "";
  if (isAmazonProductPage()) {
    const currentUrl = window.location.href;
    // Find the product ID in the URL
    const productId = currentUrl.match(/\/dp\/(\w{10})/)[1];
    productURL = `https://www.amazon.com/dp/${productId}`;
    console.log(productURL);
  } else if (isWalmartProductPage()) {
    const script = document.querySelector("#__NEXT_DATA__");
    data = JSON.parse(script.textContent);
    const productLink =
      data.props.pageProps.initialData.data.contentLayout.pageMetadata
        .pageContext.itemContext.productUrl;
    productURL = `https://www.walmart.com${productLink}`;
  }
  return productURL;
}
