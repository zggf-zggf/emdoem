$(function() {
    var timeoutIdShow;
    var timeoutIdHide;
    var popover_problem_id = -1
    var left_offset = 0;
    var top_offset = 0;
    $('body').on('mouseover', '.problem-link', function() {
        if(timeoutIdHide) {
            window.clearTimeout(timeoutIdHide)
            timeoutIdHide = null;
        }
        if (!timeoutIdShow) {
           obj = $(this)
           problem_id = obj.closest('.problem-db-entry').data('problem-id')
           if(problem_id == popover_problem_id) {
               return;
           }
           var left_offset = (obj.offset().left - 50);
           var top_offset = (obj.offset().top+30);
           timeoutIdShow = window.setTimeout(function() {
               timeoutIdShow = null
               popover_problem_id = problem_id
               $.ajax({
                   url: problem_statement_api_url.slice(0, -1) + problem_id,
                   type: "GET",
                   data: {},
                   success: function (data) {
                       console.log("success"); // another sanity check
                       if(timeoutIdHide != null) {
                           return;
                       }
                       $('body').append('<div class="p-2 shadow-sm border problem-popover text-break overflow-hidden bg-white fade-overflow" ' +
                           'style="max-width: 480px; max-height: 9lh; position: absolute; left:'+left_offset+'px; top: '+(top_offset+50)+'px; opacity: 0.2;"></div>');
                       $('.problem-popover').animate({ top: top_offset, opacity: "1" }, 200, function (x, t, b, c, d) { return -c *(t/=d)*(t-2) + b; })
                       $('.problem-popover').html(data)
                       MathJax.typeset()
                   },
                   error: function (xhr, errmsg, err) {
                       console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                   }
               });
           }, 500)
        }
    })
    $('body').on('mouseout', '.problem-link', function() {
        if(timeoutIdShow) {
            window.clearTimeout(timeoutIdShow);
            timeoutIdShow = null;
        } else {
            timeoutIdHide = window.setTimeout(function() {
                timeoutIdHide = null
                timeoutIdShow = null
                popover_problem_id = -1;
                if($('.problem-popover').length) {
                    $('.problem-popover').animate({top: $('.problem-popover').position().top + 100, opacity: "0.2"}, {
                        duration: 200, complete: function () {
                            $('.problem-popover').remove();
                        }
                    })
                }
            }, 500)
        }
    });
    $('body').on('mouseover', '.problem-popover', function() {
        if(timeoutIdHide) {
            window.clearTimeout(timeoutIdHide)
            timeoutIdHide = null;
        }
    })
    $('body').on('mouseout', '.problem-popover', function() {
        timeoutIdHide = window.setTimeout(function() {
            timeoutIdHide = null
            timeoutIdShow = null
            popover_problem_id = -1;
            if($('.problem-popover').length) {
                $('.problem-popover').animate({ top: $('.problem-popover').position().top+100, opacity: "0.2" }, {duration: 200, complete: function() {
                        $('.problem-popover').remove()
                    }})
            }
        }, 500)
    })
})