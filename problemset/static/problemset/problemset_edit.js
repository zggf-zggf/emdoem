$(function(){
    $(".sortable").sortable({
		update: function(event, ui){
			save();
		}
	});
});

function attach_edit_hover_listener(obj){
	obj.hover(function() {
		if($(this).find('.edit-name').next().css('display') == "none") {
			$(this).find('.edit-name').show()
			$(this).find('.delete-list-item').show();
		}
	}, function(){
		$(this).find('.edit-name').hide()
		$(this).find('.delete-list-item').hide();
	});
}

function attach_add_hover_listener(obj){
	obj.hover(function() {
		$(this).find('.add-problem').css('display', 'inline')
	}, function(){
		$(this).find('.add-problem').hide()
	});
}
$(function(){

	attach_edit_hover_listener($('.entry'));
	$('.editable-problemset').on("click", '.edit-name', function(){
		$(this).hide();
		$(this).prev().css("display", "none");
		$(this).next().show();
		$(this).next().next().hide();
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
	$('.editable-problemset').on('click', '.delete-list-item', function(){
		$(this).closest('.list-group-item').remove();
		save();
	})
});

function update_name_field(obj){
	if ($.trim(obj.value) == ''){
		obj.value = (obj.defaultValue ? obj.defaultValue : '');
		if(obj.value == '' && $(obj).prev().prev().html()=='') {
			$(obj).closest('.list-group-item').remove()
		}
	}
	else
	{
		$(obj).prev().prev().html(obj.value);
	}

	$(obj).hide();
	$(obj).prev().hide();
	$(obj).prev().prev().css("display", "inline");
	$(this).next().css("dipslay", "inline");
	save();
}

$(function(){
	$('#add-heading').click(function() {
		var clone = $("#headingTemplate").contents().clone();
		$(this).parent().before(clone);
		clone.find('input').show();
		clone.find('input').select();
		attach_edit_hover_listener(clone);
	});
	$('#add-comment').click(function() {
		var clone = $("#commentTemplate").contents().clone();
		$(this).parent().before(clone);
		clone.find('input').show();
		clone.find('input').select();
		attach_edit_hover_listener(clone);
	});
});

function add_problem_to_problemset(problem_id) {
	$.ajax({
		url: editable_problem_entry_url.slice(0, -1) + problem_id,
		type: "GET", // http method
		dataType: "html",
		data: {},
		success: function (data) {
			console.log("success"); // another sanity check
			$('.editable-problemset').children().last().before(data);
			attach_edit_hover_listener($('.editable-problemset').children().last().prev());
			$(obj).replaceWith("<i class=\"bi bi-check\"></i>")
			save();
		},
		error: function (xhr, errmsg, err) {
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
}
function add_toolbar_to_problem_entries(){
	$(".problem-link").parent().append("<span class='d-inline ms-1'><i class=\"add-problem bi bi-plus-square\" style='display: none; cursor: pointer;'></i></span>");
	attach_add_hover_listener($(".search-results tr"));
	$('.add-problem').click(function() {
		let problem_id = $(this).closest('.problem-db-entry').data('problem-id');
		$(this).after("<div class=\"spinner-border spinner-border-sm\" role=\"status\"></div>")
		obj = $(this).next()
		$(this).remove()
		add_problem_to_problemset(problem_id)
	});
}
function adapt_search_results(){
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
				adapt_search_results();
				add_toolbar_to_problem_entries();
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
	});
	$("#problemset-search-problem").submit(function(e){
		e.preventDefault();
		$(this).children().blur();
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
				adapt_search_results();
				add_toolbar_to_problem_entries();
			},
			// handle a non-successful response
			error: function (xhr, errmsg, err) {
				console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
			}
		});
	});
});

function parse_to_json() {
	let data = $(".editable-problemset .entry").map(function(){
		if($(this).data('type') == 'problem') {
			return {
				type: 'problem',
				name: $(this).find('a').text(),
				id: $(this).data('id')
			}
		} else if($(this).data('type') == 'comment') {
			return {
				type: 'comment',
				name: $(this).find('p').text()
			}
		} else if($(this).data('type') == 'heading') {
			return {
				type: 'heading',
				name: $(this).find('h4').text()
			}
		} else return {}
	}).get();
	return data;
}

function save() {
	$('.autosave-status').html("<div class=\"spinner-border spinner-border-sm\" role=\"status\"></div>")
	console.log("zapisuję...")
	console.log(parse_to_json())
	console.log(JSON.stringify(parse_to_json()))
	$.ajax({
		url: problemset_save_url, // the endpoint
		type: "POST", // http method
		data: {
			json: JSON.stringify(parse_to_json()),
			csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
		},
		success: function (json) {
			console.log(json); // log the returned json to the console
			console.log("success"); // another sanity check
			$('.autosave-status').html("Zapisano wszystkie zmiany.")
		},
		error: function (xhr, errmsg, err) {
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
				" <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
			console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
		}
	});
}