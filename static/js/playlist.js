const mainVideo = document.querySelector('.main-video video');
const mainVideoTitle = document.querySelector('.main-video .title');
const videoPlaylist = document.querySelector('.video-playlist .videos');

const videos = document.querySelectorAll('.video');
videos[0].classList.add('active');
videos[0].querySelector('img').src = 'images/pause.svg';

videos.forEach(selectedVideo => {
    selectedVideo.onclick = () => {
        for (let allVideos of videos) {
            allVideos.classList.remove('active');
            allVideos.querySelector('img').src = 'images/play.svg';
        }

        selectedVideo.classList.add('active');
        selectedVideo.querySelector('img').src = 'images/pause.svg';

        const videoURL = selectedVideo.dataset.url;
        mainVideo.src = videoURL;
        mainVideoTitle.innerHTML = selectedVideo.querySelector('.title').textContent;
    }
});