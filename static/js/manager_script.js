$.UIkit.support.touch = false;

Waves.attach('.btn', ['waves-button', 'waves-float']);
Waves.init();

$('textarea').each( function() {
    CKEDITOR.replace( $(this).attr('id') );
});

$('table').DataTable({
    // initComplete: function () {
    //     this.api().columns().every( function () {
    //         var column = this;
    //         var select = $('<select><option value=""></option></select>')
    //             .appendTo( $(column.footer()).empty() )
    //             .on( 'change', function () {
    //                 var val = $.fn.dataTable.util.escapeRegex(
    //                     $(this).val()
    //                 );

    //                 column
    //                     .search( val ? '^'+val+'$' : '', true, false )
    //                     .draw();
    //             } );

    //         column.data().unique().sort().each( function ( d, j ) {
    //             select.append( '<option value="'+d+'">'+d+'</option>' )
    //         } );
    //     } );
    // },
});

// $.get('/static/js/icon.json', function(data) {

//     $.map(data, function(item, index) {
//         $('.test').append('<i class="'+ index +'">'+ index +'</i>');
//     });
// });
