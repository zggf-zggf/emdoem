
$(function(){
    // bootstrap-ckeditor-fix.js
    // hack to fix ckeditor/bootstrap compatiability bug when ckeditor appears in a bootstrap modal dialog
    $.fn.modal.Constructor.prototype.enforceFocus = function() {
        modal_this = this
        $(document).on('focusin.modal', function (e) {
            if (modal_this.$element[0] !== e.target && !modal_this.$element.has(e.target).length
                && !$(e.target.parentNode).hasClass('cke_dialog_ui_input_select')
                && !$(e.target.parentNode).hasClass('cke_dialog_ui_input_text')) {
                modal_this.$element.focus()
            }
        })
    };
    $('#problemUploadModal').modal( {
        focus: false
    } );

    $('#problemUploadForm').on('submit', function(e) {
        console.log('hurra')
        var modal = $('#problemUploadModal')
        $(this).find('input[name="submit"]').addClass('invisible');
        modal.find('.spinner-border').show();
        e.preventDefault()
        $.ajax({
            url: upload_problem_url,
            type: 'POST',
            data: $(this).serialize(),
            dataType: 'json',
            success: function(response) {
                console.log(response.problem_id)
                modal.find('input[name="submit"]').removeClass('invisible');
                modal.modal('hide');
                modal.find('.spinner-border').hide();
                CKEDITOR.instances.id_problem_statement.setData('');
                add_problem_to_problemset(response.problem_id);
            },
            error: function (xhr, errmsg, err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
      });
    })
})