$(function(){
    $(".sortable").sortable();
});

function attach_hover_listener(obj){
	obj.hover(function() {
		if($(this).find('.edit-name').next().css('display') == "none") {
			$(this).find('.edit-name').show()
		}
	}, function(){
		$(this).find('.edit-name').hide()
	});
}
$(function(){

	attach_hover_listener($('.problem-item'));
	$('.editable-problemset').on("click", '.edit-name', function(){
		$(this).hide();
		$(this).prev().css("display", "none");
		$(this).next().show();
		$(this).next().select();
	});

	$('.editable-problemset').on('blur', 'input[type="text"]', function() {
		update_name_field(this);
	});

	$('.editable-problemset').on('keypress', 'input[type="text"]', function(event) {
		if (event.keyCode == '13') {
			update_name_field(this);
		}
	});
});

function update_name_field(obj){
	if ($.trim(obj.value) == ''){
		obj.value = (obj.defaultValue ? obj.defaultValue : '');
	}
	else
	{
		$(obj).prev().prev().html(obj.value);
	}

	$(obj).hide();
	$(obj).prev().hide();
	$(obj).prev().prev().css("display", "inline");
}

$(function(){
	$('#add-heading').click(function() {
		var clone = $("#headingTemplate").contents().clone();
		$(this).parent().before(clone);
		clone.find('input').show();
		clone.find('input').select();
		attach_hover_listener(clone);
	});
	$('#add-comment').click(function() {
		var clone = $("#commentTemplate").contents().clone();
		$(this).parent().before(clone);
		clone.find('input').show();
		clone.find('input').select();
		attach_hover_listener(clone);
	});
});

function replace_pagination(){
	$("#search-results-navigation").find("a").click(function(e) {
		console.log("wstepne ")
		e.preventDefault()
		$('#search-placeholder').show()
		$.ajax({
			url: $("#problemset-search-problem").prop("action") + $(this).attr('href'),
			type: "GET", // http method
			dataType: "html",
			data: {},
			success: function (data) {
				console.log("success"); // another sanity check
				$('#search-placeholder').hide();
				$('#search-results-container').empty();
				$('#search-results-container').append(data);
				replace_pagination();
			},
			// handle a non-successful response
			error: function (xhr, errmsg, err) {
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});
	});
}
$(function() {
	$("#problemset-search-problem > input").click(function() {
		$(this).select();
	})
	$("#problemset-search-problem").submit(function(e){
		e.preventDefault()
		$('#search-placeholder').show()
		$.ajax({
			url: $(this).prop('action') + "?q=" + $(this).find('input').val(),
			type: "GET", // http method
			dataType: "html",
			data: {},
			success: function (data) {
				console.log("success"); // another sanity check
				$('#search-placeholder').hide();
				$('#search-results-container').empty();
				$('#search-results-container').append(data);
				replace_pagination();
			},
			// handle a non-successful response
			error: function (xhr, errmsg, err) {
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});
	});
})