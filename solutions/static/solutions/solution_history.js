$(document).ready(function () {
    $('.solution-history-link').click(function (event){
        event.preventDefault();
        $('#solutionHistoryModal .history').empty()
        $('#solutionHistoryModal .placeholder-glow').show()
        $('#solutionHistoryModal').modal('show');
        $.ajax({
            url: $(this).attr('href'), // the endpoint
            type: "GET", // http method
            dataType: "html",
            data: {},

            // handle a successful response
            success: function (data) {
                console.log("success"); // another sanity check
                $('#solutionHistoryModal .placeholder-glow').hide()
                $('#solutionHistoryModal .history').append(data)
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    })
});
