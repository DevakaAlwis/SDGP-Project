// check for current page is amazon product page or walmart product page to display the relevent div tags
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const currentTab = tabs[0]
  if (
    (currentTab.url.includes('amazon.com') &&
      currentTab.url.includes("/dp/")) ||
    (currentTab.url.includes('walmart.com') && currentTab.url.includes('/ip/'))
  ) {
    document.getElementById('main-container').style.display = 'block'
  } else {
    document.getElementById('other-container').style.display = 'block'
  }
})

// Get the product information from storage
chrome.storage.local.get(
  [
    'productName',
    'productId',
    'productImage',
    'productPrice',
    'productSiteName',
    'productRating',
    'productReviewCount',
    'productURL',
  ],
  function (result) {
    // get the elements from the popup.html
    const productImageEl = document.getElementById('product-image')
    const productNameEl = document.getElementById('product-name')
    const productIdEl = document.getElementById('product-id')
    const productPriceEl = document.getElementById('product-price')
    const productSiteNameEl = document.getElementById('product-site')
    const productRatingEl = document.getElementById('product-rating')
    const productReviewCountEl = document.getElementById(
      'product-number-of-reviews'
    )
    const productURLEl = document.getElementById('product-url')

    // put the data in the relavent positions
    const imageURL = result.productImage;  //handle this error
    productImageEl.src = imageURL
    productNameEl.innerText = result.productName
    productIdEl.innerText = result.productId
    productPriceEl.innerText = result.productPrice
    productSiteNameEl.innerText = result.productSiteName
    productRatingEl.innerText = result.productRating
    productReviewCountEl.innerText = result.productReviewCount
    productURLEl.innerText = 'Product Link'
    productURLEl.href = result.productURL // href link
  }
)

// onclick action for button
  document.getElementById('page-button').addEventListener('click', function () {
  document.getElementById('loading-container').style.display = 'block'
  document.getElementById('main-container').style.display = 'none'
  document.getElementById('other-container').style.display = 'none'
  chrome.storage.local.get(['productName', 'productId'], function (result) {
    const productId = result.productId
    const productName = result.productName
    const object = {
      id: productId,
      name: productName
    }

    const jsonObject = JSON.stringify(object) // convert the object tp string

    // send the data to back-end
    fetch('http://localhost:5000/findProducts', {
      method: 'POST',
      credentials: 'omit', // any cookies on the page access
      headers: {
        'Content-Type': 'application/json'
      },
      body: jsonObject,
      cache: 'no-cache'
    })
      // get the response from the back-end
      .then(function (response) {
        if (response.status === 200) {
          console.log(
            `Data sent successfully | Response status: ${response.status}`
          )
          window.open('http://127.0.0.1:5000/page', '_blank')
        } else {
          console.log(`Response status: ${response.status}`)
        }
      })
      // if any error occur print it
      .catch(function (error) {
        console.log(error)
      })

    // .then((response) => {
    //   console.log("Data sent successfully");
    // })
    // .catch((error) => {
    //   console.log(error);
    // });
  })
})
