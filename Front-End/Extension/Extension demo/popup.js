// Get the product information from storage

chrome.storage.local.get(
    [
      "productName",
      "productId",
      "productImage",
      "productPrice",
      // "productSellerName",
      "productSiteName",
      "productRating",
      "productReviewCount",
      "productURL",
    ],
    function (result) {
      const productImageEl = document.getElementById("product-image");
      const productNameEl = document.getElementById("product-name");
      const productIdEl = document.getElementById("product-id");
      const productPriceEl = document.getElementById("product-price");
      // const productSellerNameEl = document.getElementById("product-seller");
      const productSiteNameEl = document.getElementById("product-site");
      const productRatingEl = document.getElementById("product-rating");
      const productReviewCountEl = document.getElementById("product-numberOfReviews");
      const productURLEl = document.getElementById("product-url");
  
      imageURL = result.productImage;
      productImageEl.src = imageURL;
      productNameEl.innerText = result.productName;
      productIdEl.innerText = result.productId;
      productPriceEl.innerText = result.productPrice;
      // productSellerNameEl.innerText = result.productSellerName;
      productSiteNameEl.innerText = result.productSiteName;
      productRatingEl.innerText = result.productRating;
      productReviewCountEl.innerText = result.productReviewCount;
      productURLEl.href = result.productURL;
      productURLEl.textContent = result.productURL;
    }
  );
  