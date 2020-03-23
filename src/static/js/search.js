document.querySelectorAll(".video").forEach(video => {
    video.addEventListener("click", function() {
        video.querySelector("#videosForm").submit();
    });
});