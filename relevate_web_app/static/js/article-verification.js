/**
 * Front end validation script for article creation.
 * Note: it puts each user's input into a dictionary with key word 'done' reflecting each
 * inputs validity.
 */


$(document).ready(function()
{
	$(".submit-button").on('click', function()	{
        try{
            if($("#id_image").val()){
	            var cropData = $image.cropper("getData");
	        }
	    }
	    catch(err){
	        console.log(err);
	    }
		var flags = {
			title: {
				done: validTitleLength(),
				message: "You must have a title between 0 and 1000 characters",
			},
			content: {
				done: validContentLength(),
				message: "Your article must have content between 0 and 5000 characters"
			},
			blurb: {
				done: validBlurbLength(),
				message: "Short description must have content between 0 and 150 characters"
			},
			references: {
				done: validReferencesLength(),
				message: "References must be less than 3000 characters"
			},
			image: {
				done: fileIsImage(),
				message: "You must upload a valid picture to display i.e file ending in png, jpeg, or jpg."
			},
			topics: {
				count: $('#selected_item input[type=checkbox]:checked').length,
				message: "You must select at least one topic",
			},
		};

		var good = true;
		var errorMsg = "<ul>";

		if (!flags.title.done)
		{
			good = false;
			errorMsg += "<li>" + flags.title.message + "</li>";
		}
		if (!flags.content.done)
		{
			good = false;
			errorMsg += "<li>" + flags.content.message + "</li>";
		}
		if(!flags.blurb.done){
			good = false;
			errorMsg += "<li>" + flags.blurb.message + "</li>";
		}

		if(!flags.references.done){
			good = false;
			errorMsg += "<li>" + flags.references.message + "</li>";
		}
		if (!flags.topics.count > 0)
		{
			good = false;
			errorMsg += "<li>" + flags.topics.message + "</li>";
		}

		if (!flags.image.done)
		{
			good = false;
			errorMsg += "<li>" + flags.image.message + "</li>";
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

	CKEDITOR.instances['id_blurb'].on('change', function(event){
		    var count = CKEDITOR.instances['id_blurb'].getData().length;
			var left = 150 - count;
			var word = left + " characters remaining";
		    $("#blurb_count").text('');
		    $("#blurb_count").text(word);
		});

	CKEDITOR.instances['id_references'].on('change', function(event){
		    var count = CKEDITOR.instances['id_references'].getData().length;
			var left = 3000 - count;
			var word = left + " characters remaining";
		    $("#references_count").text('');
		    $("#references_count").text(word);
		});

	CKEDITOR.instances['id_content'].on('change', function (event) {
    var count = CKEDITOR.instances['id_content'].getData().length;
		var left = 5000 - count;
		var word = left + " characters remaining";
    $("#content_count").text('');
    $("#content_count").text(word);
	});

	$("#id_title").keyup(function(){
		var count = $("#id_title").val().length;
		var left = 1000 - count;
		var word = left + " characters remaining";
		$("#title_count").text('');
		$("#title_count").text(word);
	});


	 /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
      $("#id_image").change(function () {
        if (this.files && this.files[0]) {
          var reader = new FileReader();
          reader.onload = function (e) {
            $("#image").attr("src", e.target.result);
            $("#modalCrop").modal("show");
          }
          reader.readAsDataURL(this.files[0]);
        }
      });

      /* SCRIPTS TO HANDLE THE CROPPER BOX */
      var $image = $("#image");
      var cropBoxData;
      var canvasData;
      $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
          viewMode: 1,
          aspectRatio: 1/1,
          minCropBoxWidth: 200,
          minCropBoxHeight: 200,
          ready: function () {
            $image.cropper("setCanvasData", canvasData);
            $image.cropper("setCropBoxData", cropBoxData);
          }
        });
      }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $image.cropper("destroy");
      });

      $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
      });

      $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
      });

      /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
      $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#modalCrop").modal("hide");
      });


});

function fileIsImage(){
	/**
	 * Checks if the upload image is a valid image.
	 * It first checks if there exist an image, then checks if user uploaded an image.
	 * @type {string[]}
     */
	var listOfExtensions = ['png', 'jpg', 'jpeg'];
	var contentVal = $("#id_image").val();
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
    if($("#id_url_image").val()){
        var contentVal = $("#id_url_image").val();
        try{
            ext = contentVal.substr(contentVal.lastIndexOf('.')+1);
        }catch (err){
            console.log(err);
        }
        if(isInArray(listOfExtensions, ext)){

             return true
        }
        if(!contentVal) {
            var currVal = $("#curr_image").attr('src');
            if (currVal) {
                return true
            }
        }
    }
	return false;
}
function isInArray(listItem, item) {
	/**
	 * Returns true if value is in arrayl
	 */
	return listItem.indexOf(item.toLowerCase()) > -1;
}

function validContentLength(){
	/**
	 * Checks to make sure content input is valid
	 * @type {Number}
     */
	var count = CKEDITOR.instances['id_content'].getData().length;
	if(count < 5000 && count > 0){
		return true
	}
	return false
}

function validReferencesLength()
{
	/**
	 * Checks to make sure references is valid
	 * @type {Number}
     */
	var c = CKEDITOR.instances['id_references'].getData().length;
	return (c < 3000);
}

function validBlurbLength()
{
	/**
	 * Checks to make sure blurb is valid.
	 * @type {Number}
     */
	var c = CKEDITOR.instances['id_blurb'].getData().length;
	return (c > 0 && c < 150);
}

function validTitleLength(){
	/**
	 * Checks to make sure title is valid
	 * @type {number|jQuery}
     */
	var count = $("#id_title").val().length;
	if(count < 5000 && count > 0){
		return true
	}
	return false
}
