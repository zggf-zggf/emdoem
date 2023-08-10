$(function() {
    $('body').on('click', '.vote-solution:not(.disabled)', function(e) {
        e.preventDefault()
        $(this).toggleClass('btn-outline-success btn-success')
        var obj = $(this)
        $.ajax({
            url: obj.prop('href'),
            method: "GET",
            success(data) {
                console.log("success");
                obj.parent().siblings().html(data.count);
            }
        })
    })
})