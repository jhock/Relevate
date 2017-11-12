var scrolled=0;

$(document).ready(function(){
        var outer = $('.outer');

        $('#right-button').click(function () {
           var leftPos = outer.scrollLeft();
           outer.animate({ scrollLeft: leftPos - 200 }, 800);
        });

        $('#left-button').click(function () {
           var leftPos = outer.scrollLeft();
           outer.animate({ scrollLeft: leftPos + 200 }, 800);
        });
});