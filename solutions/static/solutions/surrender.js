var remainingMinutes = 0;
var remainingSeconds = 0;
var endTime = new Date();
$(document).ready(function () {
    $("#surrender-btn").click(function (event){
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log("button clicked");
        $("#cancel-surrender-btn").hide();
        $.ajax({
            url: surrender_begin_url, // the endpoint
            type: "GET", // http method
            data: {},

            // handle a successful response
            success: function (json) {
                console.log("success"); // another sanity check
                location.reload();
            },

            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
        return false;
    });
    $("#surrender-as-solved-btn").click(function (event){
        event.preventDefault();
        event.stopImmediatePropagation();
        console.log("button clicked");
        $("#cancel-surrender-btn").hide();
        $.ajax({
            url: surrender_as_solved_begin_url, // the endpoint
            type: "GET", // http method
            data: {},

            // handle a successful response
            success: function (json) {
                console.log("success"); // another sanity check
                location.reload();
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
    $.getJSON( surrender_timer_url, function(json){ // the endpoint
            console.log("success"); // another sanity check
            console.log(json);
            remainingMinutes = json['remainingMinutes'];
            console.log(json.remaining_seconds);
            remainingMinutes = json.remaining_minutes;
            remainingSeconds = json.remaining_seconds;
            // Calculate the end time (current time + remaining time)
            endTime = new Date();
            endTime.setMinutes(endTime.getMinutes() + remainingMinutes);
            endTime.setSeconds(endTime.getSeconds() + remainingSeconds);

            // Start the countdown timer
            $("#timer").show();
            updateTimer(endTime);
            $("#counter-spinner").remove();
    });
}

function updateTimer(endTime) {
    const timerElement = $("#timer");

    // Update the timer every second
    (function timerCycle() {
        console.log("update timer")
        let currentTime = new Date();
        let timeDifference = endTime - currentTime;
        if(timeDifference < 0){
            location.reload();
        }

        // Check if the countdown is over
        if (timeDifference <= 0) {
            clearInterval(timerInterval);
            timerElement.text("Time's up!");
            return;
        }

        // Calculate minutes and seconds
        let minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

        // Display the remaining time
        timerElement.text(minutes + ":" + seconds.toLocaleString('en-US', {minimumIntegerDigits: 2, useGrouping:false}));
        setTimeout(timerCycle, 1000);
    })();
}
