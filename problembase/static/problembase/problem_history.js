$(document).ready(function () {
    $('.problem-history-link').click(function (event){
        event.preventDefault();
        $('#problemHistoryModal .history').empty()
        $('#problemHistoryModal .placeholder-glow').show()
        $('#problemHistoryModal').modal('show');
        $.ajax({
            url: $(this).attr('href'), // the endpoint
            type: "GET", // http method
            dataType: "html",
            data: {},

            // handle a successful response
            success: function (data) {
                console.log("success"); // another sanity check
                $('#problemHistoryModal .placeholder-glow').hide()
                $('#problemHistoryModal .history').append(data)
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    })
});
