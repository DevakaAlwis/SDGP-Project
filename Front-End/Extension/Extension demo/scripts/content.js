// Check if the current page is an Amazon or walmart product page
if (isAmazonProductPage() || isWalmartPage()) {
    // Get the product name and ID from the page
    // const productLink = tabs[0].url;
    const productName = getProductName();
    const productId = getProductId();
    const productImage = getProductImage();
    const productPrice = getProductPrice();
    const productSellerName = getProductSellerName();
    const productSiteName = getProductSiteName();
    const productRating = getProductRating();
    const productReviewCount = getProductReviewCount();
    const productURL = getProductURL();
    console.log(
      productName,
      productId,
      productImage,
      productPrice,
      productSellerName,
      productSiteName,
      productRating,
      productReviewCount,
      productURL
    );
    // Display the product information in the extension popup
    chrome.runtime.sendMessage({
      type: "PRODUCT_INFO",
      // productLink: productLink,
      productName: productName,
      productId: productId,
      productImage: productImage,
      productPrice: productPrice,
      productSellerName: productSellerName,
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
  function isWalmartPage() {
    return (
      window.location.href.includes("walmart") &&
      window.location.href.includes("/ip/")
    );
  }
  
  // Function to get the product name from the page
  function getProductName() {
    let productName = "";
    if (isAmazonProductPage()) {
      productName = document.getElementById("productTitle").innerText.trim();
    } else if (isWalmartPage()) {
      productName = document.getElementById("vi-lkhdr-itmTitl").innerText.trim();
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
    } else if (isWalmartPage()) {
      const walmartRegex = /\/(\d+)\?/;
      const matches = walmartRegex.exec(window.location.href);
      productId = matches[1];
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
    } else if (isWalmartPage()) {
      productImage = document.querySelector('[data-testid="zoom-image"] img').getAttribute('src');
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
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productPrice;
  }
  
  // Function to get the product Seller Name from the page
  function getProductSellerName() {
    let productSellerName = "";
    if (isAmazonProductPage()) {
      productSellerName = document.getElementById("bylineInfo").innerText.trim();
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productSellerName;
  }
  
  // Function to get the product Site Name from the page
  function getProductSiteName() {
    let productSiteName = "";
    if (isAmazonProductPage()) {
      if (window.location.hostname.includes("amazon.com")) {
        productSiteName = "Amazon";
      }
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productSiteName;
  }
  
  // Function to get the product Link from the page
  function getProductLink() {
    let productLink = "";
    if (isAmazonProductPage()) {
      if (window.location.hostname.includes("amazon.com")) {
        productLink = window.location.href;
      }
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productLink;
  }
  
  // Function to get the product Rating from the page
  function getProductRating() {
    let productRating = "";
    if (isAmazonProductPage()) {
      const titleElement = document.querySelector("#acrPopover");
      productRating = titleElement.getAttribute("title");
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productRating;
  }
  
  // Function to get the product Review Count from the page
  function getProductReviewCount() {
    let ratingValue = "";
    if (isAmazonProductPage()) {
      const productReviewCount = document
        .getElementById("acrCustomerReviewText")
        .innerText.trim();
      const ratingWithoutComma = productReviewCount.replace(",", "");
      ratingValue = parseInt(ratingWithoutComma);
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return ratingValue;
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
    } else if (isWalmartPage()) {
      // productPrice = document
      //   .getElementById("imgTagWrapperId")
      //   .getElementsByTagName("img")[0].src;
    }
    return productURL;
  }
  