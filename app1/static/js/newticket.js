$(document).ready(function() {
    $('#summernote').summernote();
});

/*para dejar solo habilitadas los botones fuentes*/

/*
$('#summernote').summernote({
    toolbar: [
        // [groupName, [list of button]]
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['font', ['strikethrough', 'superscript', 'subscript']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']]
    ]
});
*/

$('#summernote').summernote({
    placeholder: 'Descripción',
    height: 100,
    tabsize: 2
})