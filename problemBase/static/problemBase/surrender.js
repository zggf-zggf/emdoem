var remainingMinutes = 0;
var remainingSeconds = 0;
$(document).ready(function () {
    $("#surrender-btn").click(function (event){
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log("button clicked");
        $.ajax({
            url: surrender_begin_url, // the endpoint
            type: "GET", // http method
            data: {},

            // handle a successful response
            success: function (json) {
                console.log("success"); // another sanity check
                show_timer();
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });
});
function show_timer() {
    $.get({
        url: surrender_timer_url, // the endpoint
        type: "GET", // http method
        data: {},

        success: function (json) {
            console.log("success"); // another sanity check
            remainingMinutes = json.remainingMinutes
            remainingSeconds = json.remainingSeconds
            // Calculate the end time (current time + remaining time)
            const endTime = new Date();
            endTime.setMinutes(endTime.getMinutes() + remainingMinutes);
            endTime.setSeconds(endTime.getSeconds() + remainingSeconds);

            // Start the countdown timer
            $("#timer").show();
            $("#surrender-modal-close").click();
            updateTimer(endTime);
        },

        error: function (xhr, errmsg, err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    // Get the remaining time from Django template variable (you can set this in the template)

}

function updateTimer(endTime) {
    const timerElement = $("#timer");

    // Update the timer every second
    const timerInterval = setInterval(function () {
        console.log("update timer")
        const currentTime = new Date();
        const timeDifference = endTime - currentTime;

        // Check if the countdown is over
        if (timeDifference <= 0) {
            clearInterval(timerInterval);
            timerElement.text("Time's up!");
            return;
        }

        // Calculate minutes and seconds
        const minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

        // Display the remaining time
        timerElement.text(minutes + " minutes and " + seconds + " seconds");
    }, 1000); // Update the timer every second
}
