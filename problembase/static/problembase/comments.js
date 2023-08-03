var submit_btn;
$(document).ready(function () {
    $("#commentForm").hide();
    $(".add-comment").click(function () {
        $("#commentForm").show();
        $("#commentForm").detach().appendTo($(this).parent().parent());
        console.log($(this).parent().children('input').eq(0).val());
        $("#comment-form-solution-id").val($(this).parent().children('input').eq(0).val());
        $(".add-comment").show();
        $(this).hide();
    });
    $('#commentForm').on('submit', function (event) {
        event.preventDefault();
        console.log("form submitted!")  // sanity check
        $('#comment-content').prop('disabled', true)
        submit_btn = $('[name="submit-comment"]').replaceWith($("<div class='spinner-border spinner-border-sm' id='spinner'></div>"));
        create_comment();
    });
});

function create_comment() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url: url, // the endpoint
        type: "POST", // http method
        data: {
            the_comment: $('#comment-content').val(),
            solution_id: $("#comment-form-solution-id").val(), // data sent with the post request
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
        },

        // handle a successful response
        success: function (json) {
            $('#comment-content').prop('disabled', false)
            $('#spinner').replaceWith(submit_btn);
            $('#commentForm').parent().append(($("<h4>Zapisano komentarz!</h4>")));
            $('#comment-content').val('');
            $('#commentForm').hide();
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error: function (xhr, errmsg, err) {
            $('#spinner').hide();
            $('#commentForm').parent().append("<p class='text-danger'>Błąd</p>");
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
