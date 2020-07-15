$(document).ready(function (e) {
    $('.navbarSupportedContent').click(function () {

        var toggle_sign = $(this).find(".toggle_sign");
        if ($(toggle_sign).hasClass("fa-window-restore")) {
            $(toggle_sign).removeClass("fa-window-restore").addClass("fa-list");
        } else {
            $(toggle_sign).addClass("fa-list").removeClass("fa-window-restore");
        }
        // or toggle event you can use.
        //$(toggle_sign).toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
    });
});