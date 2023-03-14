//console.log("content.js");
(() => {
 let youtubeLefControls, youtubePlayer;

 chrome.rintime.onMessage.addlistener((obj, sender)) => {
    const { type, value, videoId } = obj;

    if(type === "NEW") {
        currentvideo == videoId;
        newVideoLoaded();
    }
 });


 
})();