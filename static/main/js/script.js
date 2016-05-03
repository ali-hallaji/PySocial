// set direction on modal
$.UIkit.langdirection = UIkit.$html.attr("dir") == "rtl" ? "left" : "right";

// $('.uk-modal').on({

//     'show.uk.modal': function(){
//         $('body').css({
//             'padding-left': '0px',
//             'padding-right': '15px'
//         });
//     },

//     'hide.uk.modal': function(){
//         $('body').removeAttr('style');
//     }
// });


// $('.tm-accordion-content').on({

//     'toggle.uk.acordion': function (event, active, toggle, content) {
//         $('.tm-panel-course').removeClass('uk-active');
//         $('.tm-panel-course').not('.uk-active').html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>').next().html('نمایش لیست <i class="uk-icon-chevron-down"></i>');
//         content.parents('.tm-panel-course').addClass('uk-active');

//         if (active) {
//             toggle.find('a.uk-hidden').html('نمایش لیست <i class="uk-icon-chevron-down"></i>').next().html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>');
//         }
//     }
// });

$('.toggle-btn.uk-active').children('a:not(.uk-hidden)').html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>');
$('.toggle-btn').on('click', function() {
    $('.toggle-btn.uk-active').children('a:not(.uk-hidden)').html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>');
});