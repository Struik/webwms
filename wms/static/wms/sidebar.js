$(document).ready(function () {
    var trigger = $('.hamburger'),
    overlay = $('.overlay'),
    isClosed = true;
    console.log(isClosed);

    trigger.click(function () {
      hamburger_cross();
    });

    function hamburger_cross() {
        if (isClosed == true) {
            console.log(1);
            overlay.hide();
            trigger.removeClass('is-closed');
            trigger.addClass('is-open');
            isClosed = false;
        } else {
            console.log(2);
            overlay.show();
            trigger.removeClass('is-open');
            trigger.addClass('is-closed');
            isClosed = true;
        }
    }

    $('[data-toggle="offcanvas"]').click(function () {
        $('#wrapper').toggleClass('toggled');
    });
});