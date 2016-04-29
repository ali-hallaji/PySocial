// $('.uk-modal').on({

//     'show.uk.modal': function(){
//         $('body').css({
//             'padding-left': '',
//             'padding-right': '15px'
//         });
//     },

//     'hide.uk.modal': function(){
//         $('body').css({
//             'padding-left': '',
//             'padding-right': '15px'
//         });
//     }
// });

// var sticky = UIkit.sticky('header', {
//     media: 767,
//     top: ".uk-sticky-placeholder + *",
//     animation: "uk-animation-slide-top"
// });

$('.tm-accordion-content').on({

    'toggle.uk.accordion': function (event, active, toggle, content) {
        $('.tm-panel-course').removeClass('uk-active');
        $('body .toggle-btn').find('a.uk-hidden').html('نمایش لیست <i class="uk-icon-chevron-down"></i>').next().html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>');
        content.parents('.tm-panel-course').addClass('uk-active');

        if (active) {
            toggle.find('a.uk-hidden').html('نمایش لیست <i class="uk-icon-chevron-down"></i>').next().html('پنهان کردن لیست <i class="uk-icon-chevron-up"></i>');
        }
    }
});