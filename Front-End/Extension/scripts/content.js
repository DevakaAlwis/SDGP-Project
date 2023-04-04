/* global chrome */
// Check if the current page is an Amazon or walmart product page
if (isAmazonProductPage() || isWalmartProductPage()) {
  const productNameV = getProductName() // Get the product name
  const productIdV = getProductId() // Get the product id
  const productImageV = getProductImage() // Get the product Image URL
  const productPriceV = getProductPrice() // Get the product Price
  const productSiteNameV = getProductSiteName() // Get the prodict site name
  const productRatingV = getProductRating() // Get the product rating
  const productReviewCountV = getProductReviewCount() // Get the product review count
  const productURLV = getProductURL() // Get the product URL
  console.log(
    productNameV,
    productIdV,
    productImageV,
    productPriceV,
    productSiteNameV,
    productRatingV,
    productReviewCountV,
    productURLV
  ) // Print the details in the console log
  // Display the product information in the extension popup
  chrome.runtime.sendMessage({
    type: 'PRODUCT_INFO',
    productId: productIdV,
    productName: productNameV,
    productImage: productImageV,
    productPrice: productPriceV,
    productSiteName: productSiteNameV,
    productRating: productRatingV,
    productReviewCount: productReviewCountV,
    productURL: productURLV
  })
}

// Function to check if the current page is an Amazon product page
function isAmazonProductPage () {
  return (
    window.location.hostname.includes('amazon.com') &&
    window.location.pathname.includes('/dp/')
  )
}

// Function to check if the current page is an walmart product page
function isWalmartProductPage () {
  return (
    window.location.hostname.includes('walmart.com') &&
    window.location.pathname.includes('/ip/')
  )
}

// Function to get the product name from the page
function getProductName () {
  let productName = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const productTitleElement = document.getElementById('productTitle') // Get the product title element
    // Check if the product title is exist or not
    if (productTitleElement) {
      productName = productTitleElement.innerText.trim()
    }
    // Check if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__') // Get the json script
    // Check if the script is exists
    if (script) {
      const json = JSON.parse(script.textContent)
      // Check if the name is exists
      if (
        json.props.pageProps.initialData.data.contentLayout.pageMetadata
          .pageContext.itemContext.name
      ) {
        productName =
          json.props.pageProps.initialData.data.contentLayout.pageMetadata
            .pageContext.itemContext.name
      }
    }
  }
  return productName
}

// Function to get the product ID from the page
function getProductId () {
  let productId = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const asinRegex = /dp\/(\w{10})/ // regular expression for get the asin value
    const matches = asinRegex.exec(window.location.href) // match the value and save it
    productId = matches[1]
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__')
    const json = JSON.parse(script.textContent)
    productId =
      json.props.pageProps.initialData.data.contentLayout.pageMetadata
        .pageContext.itemContext.itemId // get the itemId
  }
  return productId
}

// Function to get the product Image Link from the page
function getProductImage () {
  let productImage = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const productImageElement = document.getElementById('imgTagWrapperId') // Get the product image element
    if (productImageElement) {
      productImage = productImageElement.getElementsByTagName('img')[0].src
    }
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__') // Get the json script
    const json = JSON.parse(script.textContent)
    // Check if the json is exists
    if (
      json.props.pageProps.initialData.data.product.imageInfo.allImages[0].url
    ) {
      productImage =
        json.props.pageProps.initialData.data.product.imageInfo.allImages[0]
          .url
    }
  }
  return productImage
}

// Function to get the product Price from the page
function getProductPrice () {
  let productPrice = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const priceElement = document.getElementsByClassName(
      'reinventPricePriceToPayMargin'
    )[0] // Get the product price element
    if (priceElement) {
      productPrice = priceElement
        .querySelector('.a-offscreen')
        .innerText.trim()
    }
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__') // Get the json script
    const json = JSON.parse(script.textContent)

    const current = json.props.pageProps.initialData.data.product.priceInfo // get the priceInfo  object
    // Check if the current price is exists
    if (current.currentPrice != null) {
      productPrice = current.currentPrice.priceString
      // Check if the subscription price is exists
    } else if (current.subscriptionPrice != null) {
      productPrice = current.subscriptionPrice.priceString
    }
  }
  return productPrice
}

// Function to get the product Site Name from the page
function getProductSiteName () {
  let productSiteName = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    if (window.location.hostname.includes('amazon.com')) {
      productSiteName = 'Amazon'
    }
  } else if (isWalmartProductPage()) {
    productSiteName = 'Walmart'
  }
  return productSiteName
}

// Function to get the product Rating from the page
function getProductRating () {
  let productRating = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const titleElement = document.querySelector('#acrPopover') // Get the product rating element
    if (titleElement) {
      productRating = titleElement.getAttribute('title')
    }
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__') // Get the json script
    const json = JSON.parse(script.textContent)
    // Check if the rating is exists
    if (json.props.pageProps.initialData.data.reviews.averageOverallRating) {
      productRating =
        json.props.pageProps.initialData.data.reviews.averageOverallRating
    }
  }
  return productRating
}

// Function to get the product Review Count from the page
function getProductReviewCount () {
  let reviewCount = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const productReviewCountElement = document.getElementById(
      'acrCustomerReviewText'
    ) // Get the product review count element
    if (productReviewCountElement) {
      const productReviewCount = productReviewCountElement.innerText.trim()
      const ratingWithoutComma = productReviewCount.replace(',', '') // replace the 12,000 comma with nothing
      reviewCount = parseInt(ratingWithoutComma) // convert it to integer
    }
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__') // Get the json script
    const json = JSON.parse(script.textContent)
    // Check if the review count is exists
    if (json.props.pageProps.initialData.data.reviews.totalReviewCount) {
      reviewCount =
        json.props.pageProps.initialData.data.reviews.totalReviewCount
    }
  }
  return reviewCount
}

// Function to get the product URL from the page
function getProductURL () {
  let productURL = ''
  // Check  if it is an amazon page
  if (isAmazonProductPage()) {
    const currentUrl = window.location.href
    // Find the product ID in the URL
    const productId = currentUrl.match(/\/dp\/(\w{10})/)[1] // match the current url with the regular expression check /dp/ 10words and get the 10 words
    productURL = `https://www.amazon.com/dp/${productId}` // concat the productLink with asin
    // Check  if it is a walmart page
  } else if (isWalmartProductPage()) {
    const script = document.querySelector('#__NEXT_DATA__')
    const json = JSON.parse(script.textContent)
    // Check if the URL link is exists
    if (
      json.props.pageProps.initialData.data.contentLayout.pageMetadata
        .pageContext.itemContext.productUrl
    ) {
      const productLink =
        json.props.pageProps.initialData.data.contentLayout.pageMetadata
          .pageContext.itemContext.productUrl
      productURL = `https://www.walmart.com${productLink}` // concat the productLink with walmart link
    }
  }
  return productURL
}
