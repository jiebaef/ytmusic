$(function() {
    divs = ["startSelenium", "pausePlay", "skipSong"];
    divs.forEach(div => {
        $('div#' + div).bind('click', function() {
            $.getJSON('/' + div,
                function(data) {
                    //do nothing
                });
            return false;
        });
    })
});