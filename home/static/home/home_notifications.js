$(function(){
    $('#problemsetEditUnregister').click(function(){
        $(this).closest('.card').remove()
        $.ajax({
            url: unregister_problemset_editing_notification_url,
            type: "GET", // http method
            dataType: "html",
            data: {},
            success: function (data) {
                console.log("success"); // another sanity check
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    });
})