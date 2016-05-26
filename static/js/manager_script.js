$(document).ready(function() {

});
$('table').DataTable();
$('div#DataTables_Table_0_paginate')
    .children('ul')
    .attr('class', 'uk-pagination uk-pagination-left');

$('#DataTables_Table_0_previous')
    .find('.uk-icon-angle-left')
    .attr('class', 'uk-icon-angle-right');

$('#DataTables_Table_0_next')
    .find('.uk-icon-angle-right')
    .attr('class', 'uk-icon-angle-left');