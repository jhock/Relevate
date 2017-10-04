/**
 * Front end validation script for link creation.
 * Note: it puts each user's input into a dictionary with key word 'done' reflecting each
 * inputs validity.
 */

$(document).ready(function()
{
	$('.submit-button').on('click', function () {
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
				done: $("#id_title").val().length,
				message: "You must have a title.",
			},
			link: {
				done: $('#id_link').val().length,
				message: "You must have a link.",
			},
			blurb: {
				done: validContentLength(),
				message: "You must have a description between 0 and 400 characters long",
			},
			topics: {
				count: $('#id_topic_choices input[type=checkbox]:checked').length,
				message: "You must select at least one topic",
			},
			image: {
				done: fileIsImage(),
				message: "You must upload a valid picture to display i.e file ending in png, jpeg, or jpg."
			},
		};
		var good = true;
		var errorMsg = "<ul>";
		if (!flags.title.done)
		{
			good = false;
			errorMsg += "<li>" + flags.title.message + "</li>"
		}
		if (!flags.link.done)
		{
			good = false;
			errorMsg += "<li>" + flags.link.message + "</li>"
		}
		if (!flags.blurb.done)
		{
			good = false;
			errorMsg += "<li>" + flags.blurb.message + "</li>"
		}
		if (flags.topics.count == 0)
		{
			good = false;
			errorMsg += "<li>" + flags.topics.message + "</li>"
		}
		if (!flags.image.done)
		{
			good = false;
			errorMsg += "<li>" + flags.image.message + "</li>"
		}
		if ($(this).attr('name') == 'save_and_publish')
		{
			$('#hidden-checkbox').prop('checked', true);
		}
		if (good)
		{
			$('#load-icon').removeClass('invisible');
			$('#link-form').submit();
		}
		else
		{
			UIkit.modal.alert(errorMsg + "</ul>");
		}
	});

	CKEDITOR.instances['id_blurb'].on('key', function(event){
		    var count = CKEDITOR.instances['id_blurb'].getData().length;
			var left = 400 - count;
			var word = "(" + left + " characters left )";
		    $("#blurb_count").text('');
		    $("#blurb_count").text(word);
	});

	$("#id_title").keyup(function(){
		var count = $("#id_title").val().length;
		var left = 1000 - count;
		var word = "(" + left + " characters left )";
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

function validContentLength(){
	/**
	 * Checks if the content length for description is valid
	 * @type {Number}
     */
	var count = CKEDITOR.instances['id_blurb'].getData().length;
	if(count < 400 && count > 0){
		return true
	}
	return false
}

function fileIsImage(){
	/**
	 * Checks if the upload image is a valid image
	 *  * It first checks if there exist an image, then checks if user uploaded an image.
	 * @type {string[]}
     */
		var listOfExtensions = ['png', 'jpg', 'jpeg'];
		var contentVal = $("#id_image").val();
		var ext = "";
		try{
			ext = contentVal.substr(contentVal.lastIndexOf('.')+1);
		}catch (err){

		}
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