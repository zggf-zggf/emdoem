$(function() {
    problem_statement = $("#problem-statement");
    if (problem_statement.prop('scrollHeight') > problem_statement.height() ) {
        problem_statement.after("<a id='show-statement' href='#' class='w-100 fs-5 flex-row justify-content-center text-decoration-none' style='display: flex;'>. . .</a>")
        problem_statement.after("<a id='hide-statement' href='#' class='w-100 fs-5 flex-row justify-content-center text-decoration-none' style='display: none;'>Zwiń ^</a>")
        $("#show-statement").click(function(e) {
            e.preventDefault()
            problem_statement.css('max-height', '')
            $(this).css('display', 'none')
            $('#hide-statement').css('display', 'flex')
        })
        $("#hide-statement").click(function(e) {
            e.preventDefault()
            problem_statement.css('max-height', '9lh')
            $(this).css('display', 'none')
            $('#show-statement').css('display', 'flex')
        })
    }
})