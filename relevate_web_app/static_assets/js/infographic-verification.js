/**
 * Front end validation script for Infographic creation.
 * Note: it puts each user's input into a dictionary with key word 'done' reflecting each
 * inputs validity.
 */

$(document).ready(function()
{
	$(".submit-button").on('click', function()
	{
		var flags = {
			title: {
				done: $("#id_title").val().length > 0,
				message: "You must have a title with character length between 0 and 1000",
			},
			blurb: {
				done: validBlurbLength(),
				message: "Description must be between 1 and 150 characters"
			},
			file: {
				done: fileIsImage(),
				message: "You must select an infographic to upload i.e file ending in png, jpeg, or jpg."
			},
			topics: {
				count: $('#selected_item input[type=checkbox]:checked').length,
				message: "You must select at least one topic"
			},
		};

		var good = true;
		var errorMsg = "<ul>";

		if (!flags.title.done)
		{
			good = false;
			errorMsg += "<li>" + flags.title.message + "</li>";
		}
		if (!flags.file.done)
		{

			good = false;
			errorMsg += "<li>" + flags.file.message + "</li>";
		}
		if (!flags.blurb.done)
		{

			good = false;
			errorMsg += "<li>" + flags.blurb.message + "</li>";
		}
		if (!flags.topics.count > 0)
		{
			good = false;
			errorMsg += "<li>" + flags.topics.message + "</li>";
		}

		if ($(this).attr('name') == "save_and_publish")
		{
			$("#hidden-publish-checkbox").prop('checked', true);
		}

		if (good)
		{
			$('form').submit();
		}
		else
		{
			UIkit.modal.alert(errorMsg + "</ul>");
		}
	});

	CKEDITOR.instances['id_blurb'].on('key', function(event){
		    var count = CKEDITOR.instances['id_blurb'].getData().length;
			var left = 150 - count;
			var word = "(" + left + " characters left )";
		    $("#blurb_count").text('');
		    $("#blurb_count").text(word);
		});

	$("#id_title").keyup(function(){
		var count = $("#id_title").val().length;
		var left = 1000 - count;
		var word = "(" + left + " characters left )";
		console.log("little break!");
		$("#title_count").text('');
		$("#title_count").text(word);
	});

});

function fileIsImage(){
	var listOfExtensions = ['png', 'jpg', 'jpeg'];
	var contentVal = $("#id_contents").val();
	var ext = "";
	try{
		ext = contentVal.substr(contentVal.lastIndexOf('.')+1);
	}catch (err){

	}
	console.log(contentVal, ext);
	if(isInArray(listOfExtensions, ext)){

		 return true
	}
	if(!contentVal) {
		var currVal = $("#curr_image").attr('src');
		console.log("content val ", currVal);
		if (currVal) {

			return true
		}
	}
	return false;
}
function isInArray(days, day) {
    return days.indexOf(day.toLowerCase()) > -1;
}

function validBlurbLength()
{
	var c = CKEDITOR.instances['id_blurb'].getData().length;
	return (c > 0 && c < 150);
}