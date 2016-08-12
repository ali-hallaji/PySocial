// search custom template nad functions
UIkit.on('beforeready.uk.dom', function(){

    $.extend(UIkit.components.search.prototype.defaults, {
        renderer: function(data) {

                var $this = this, opts = this.options;

                this.dropdown.removeClass().append(this.template({"items": (data || []), "msgResultsHeader":opts.msgResultsHeader, "msgMoreResults": opts.msgMoreResults, "msgNoResults": opts.msgNoResults}));
                this.show();
            },
            template:   '<div class="uk-block uk-contrast">\
                            <div class="uk-grid" data-uk-grid-margin>\
                                <div class="uk-width-small-1-1 uk-width-medium-1-2 uk-width-large-1-3">\
                                    <div class="tm-panel-saerch uk-panel">\
                                        <h3 class="uk-panel-title"><i class="uk-icon-users uk-margin-small-left"></i><b>کاربران</b></h3>\
                                        {{#items.users && items.users.length}}\
                                            <ul class="tm-list-result uk-list" data-uk-margin>\
                                                {{~items.users}}\
                                                    <li>\
                                                        <a class="uk-flex uk-flex-middle" href="{{{$item.href}}}">\
                                                            <img class="uk-margin-small-left uk-border-circle" width="64" src="{{$item.picture}}" alt="{{$item.username}}">\
                                                            {{$item.first_name}} {{$item.last_name}}\
                                                            {{$item.username}}\
                                                        </a>\
                                                    </li>\
                                                {{/items}}\
                                            </ul>\
                                        {{/end}}\
                                        {{^items.users.length}}\
                                            <div class="tm-no-result">کاربری یافت نشد</div>\
                                        {{/end}}\
                                    </div>\
                                </div>\
                                <div class="uk-width-small-1-1 uk-width-medium-1-2 uk-width-large-2-3">\
                                    <div class="tm-panel-saerch uk-panel">\
                                        <h3 class="uk-panel-title"><i class="uk-icon-file-text uk-margin-small-left"></i><b>مطالب مربوطه</b></h3>\
                                        {{#items.lessons && items.lessons.length && items.contents && items.contents.length}}\
                                            <ul class="tm-list-result uk-list" data-uk-margin>\
                                                {{~items.lessons}}\
                                                    <li>\
                                                        <a class="uk-flex uk-flex-middle" href="{{{$item.href}}}">\
                                                            <img class="uk-margin-left uk-flex-item-none" width="64" src="/media/dashboard/box/{{$item.box_id}}.png" alt="">\
                                                            {{{$item.body}}}\
                                                        </a>\
                                                    </li>\
                                                {{/items}}\
                                                {{~items.contents}}\
                                                    <li>\
                                                        <a class="uk-flex uk-flex-middle" href="{{{$item.href}}}">\
                                                            <img class="uk-margin-left uk-flex-item-none" width="64" src="/media/dashboard/box/{{$item.box_id}}.png" alt="">\
                                                            {{{$item.description}}}\
                                                        </a>\
                                                    </li>\
                                                {{/items}}\
                                            </ul>\
                                        {{/end}}\
                                        {{^items.contents.length}}\
                                            <div class="tm-no-result">مطلبی یافت نشد</div>\
                                        {{/end}}\
                                    </div>\
                                </div>\
                            </div>\
                        </div>'
    });
});

// set direction on modal
$.UIkit.langdirection = UIkit.$html.attr("dir") == "rtl" ? "left" : "right";

// notifucation function
function uikitNotify(message, icon, status, timeout, pos){
    UIkit.notify({
        message : " <div class='uk-flex uk-flex-middle'>\
                        <i class='uk-icon-"+ icon +"'></i>\
                        "+ message +"\
                    </div>",
        status  : typeof status == 'undefined'?'info':status,
        timeout : typeof timeout == 'undefined'?5000:timeout,
        pos     : typeof pos == 'undefined'?'top-center':pos
    });
}

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

// datatble
$('.datatable').DataTable({
    "language": {
        "url": "//cdn.datatables.net/plug-ins/1.10.12/i18n/Persian.json"
    }
});