$(document).ready(function()
{
	$(".submit-button").on('click', function()	{

		var flags = {
			content: {
				done: validContentLength(),
				message: "Your article must have content between 0 and 1500 characters"
			},
			name: {
				done: validName(),
				message: "You must include a name less than 150 characters"
			},
			type_of_entry: {
				done: typeChecked(),
				message: "You must select the section that the entry will be added to"
			}
		};

		var good = true;
		var errorMsg = "<ul>";


		if (!flags.content.done)
		{
			good = false;
			errorMsg += "<li>" + flags.content.message + "</li>";
		}
		if (!flags.name.done)
		{
			good = false;
			errorMsg += "<li>" + flags.name.message + "</li>";
		}
		if (!flags.type_of_entry.done)
		{
			good = false;
			errorMsg += "<li>" + flags.type_of_entry.message + "</li>";
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

	CKEDITOR.instances['id_content'].on('key', function(event){
		    var count = CKEDITOR.instances['id_content'].getData().length;
			var left = 1500 - count;
			var word = "(" + left + " characters left )";
		    $("#content_count").text('');
		    $("#content_count").text(word);
		});

	$("#id_title").keyup(function(){
		var count = $("#id_title").val().length;
		var left = 100 - count;
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
          aspectRatio: 3/4,
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

function typeChecked(){
    /**
	 * Checks if any of the funder_or_adviser radio buttons are checked.
     */
	if ( $('[id^=id_funder_or_adviser]').is(':checked') ) {
		return true;
	}
	else {
		console.log($('funder_or_adviser').is(':checked'));
		return false;
	}
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
	if(count < 1500 && count > 0){
		return true
	}
	return false
}

function validName(){
	/**
	 * Checks to make sure name input is valid
	 * @type {Number}
     */
	var count = $("#id_name").val().length;
	if(count < 150 && count > 0){
		return true
	}
	return false
}

function validTitleLength(){
	/**
	 * Checks to make sure title is valid
	 * @type {number|jQuery}
     */
	var count = $("#id_title").val().length;
	if(count < 100 && count > 0){
		return true
	}
	return false
}

