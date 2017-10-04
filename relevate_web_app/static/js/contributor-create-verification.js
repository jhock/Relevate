/**
 * Front end validation script for contributor creation.
 * Note: it puts each user's input into a dictionary with key word 'done' reflecting each
 * inputs validity.
 */

$(document).ready(function()
{
    console.log("hello");
	verificationFlags = {
		mentor: {
			sectionDone: false,
			sectionNeeded: false,
			message: "Your level of degree requires a mentor. Please select one.",
		},
		degrees: {
			sectionDone: false,
			counter: 0,
			message: "You must have at least 1 degree. Are you sure you clicked the add button?",
		},
		topics: {
			sectionDone: false,
			counter: $('#id_area_of_expertise input[type=checkbox]:checked').length,
			message: "You must select at least 1 expertise topic",
		},
		professional_info: {
			sectionDone: false,
			elems: {
				address: {
					done: $("#id_address").val().length > 0,
					message: "You must enter an address",
				},
				city: {
					done: $("#id_city").val().length > 0,
					message: "You must enter a city",
				},
				zip: {
					done: $("#id_zipcode").val().length > 0,
					message: "You must enter a zip code.",
				},
				biography: {
					done: $("#id_biography").val().length > 0,
					message: "You must complete the professional interests section",
				},
			},
		},
		terms: {
			sectionDone: $('#id_accept_terms').prop('checked'),
			elems: {
				checkbox: {
					done: $('#id_accept_terms').prop('checked'),
					message: "You must accept the terms and conditions.",
				}
			}
		},
	};

	function verifySection(section)
	{
		for (var key in section.elems)
		{
			if (section.elems.hasOwnProperty(key))
			{
				if (!section.elems[key].done)
				{
					section.sectionDone = false;
					return false;
				}
			}
		}
		section.sectionDone = true;
		return true;
	}

	function markSection(done_id, incomplete_id, completed)
	{
		if (done_id != undefined && incomplete_id != undefined)
		{
			if (completed)
			{
				$(done_id).show();
				$(incomplete_id).hide();
			}
			else
			{
				$(incomplete_id).show();
				$(done_id).hide();
			}
		}
	}

	function verifyTextInput(len, section, key, done_id, incomplete_id)
	{
		if (len > 0)
		{
			verificationFlags[section].elems[key].done = true;
			if (verifySection(verificationFlags[section]))
			{
				markSection(done_id, incomplete_id, true);
			}
		}
		else
		{
			verificationFlags[section].elems[key].done = false;
			if (!verifySection(verificationFlags[section]))
			{
				markSection(done_id, incomplete_id, false);
			}
		}
	}

	$('.expertise-checkbox').on('change', function()
	{
		var len = $('#id_area_of_expertise input[type=checkbox]:checked').length;
		verificationFlags.topics.counter = len;
		if (len > 0)
		{
			markSection("#topics-done", "#topics-incomplete", true);
		}
		else
		{
			markSection("#topics-done", "#topics-incomplete", false);
		}
	});

	/*
		I know this is hacky and bad. Don't judge me. NJ
	*/
	setInterval(checkDegreeLen, 1000);
	function checkDegreeLen()
	{
		verificationFlags.degrees.counter = $("#acaProf tr.acaRow").length;
		if (verificationFlags.degrees.counter == 0)
		{
			markSection("#degree-done", "#degree-incomplete", false);
		}
		else
		{
			markSection("#degree-done", "#degree-incomplete", true);
		}
	}

	$("#id_address").on('keyup', function()
	{
		var len = $(this).val().length;
		verifyTextInput(len, 'professional_info', 'address', 
			'#professional-info-done', '#professional-info-incomplete');
	});

	$("#id_city").on('keyup', function()
	{
		var len = $(this).val().length;
		verifyTextInput(len, 'professional_info', 'city', 
			'#professional-info-done', '#professional-info-incomplete');
	});

	$("#id_zipcode").on('keyup', function()
	{
		var len = $(this).val().length;
		verifyTextInput(len, 'professional_info', 'zip', 
			'#professional-info-done', '#professional-info-incomplete');
	});

	$("#id_biography").on('keyup', function()
	{
		var len = $(this).val().length;
		verifyTextInput(len, 'professional_info', 'biography',
			'#professional-info-done', '#professional-info-incomplete');
	});

	$('#id_accept_terms').on('change', function()
	{
		if ($(this).prop("checked"))
		{
			verificationFlags.terms.elems.checkbox.done = true;
			verificationFlags.terms.sectionDone = true;
			$('#terms-done').show()
			$('#terms-incomplete').hide();
		}
		else
		{
			verificationFlags.terms.elems.checkbox.done = false;
			verificationFlags.terms.sectionDone = false;
			$('#terms-done').hide();
			$('#terms-incomplete').show();
		}
	});

	$('#id_adviser').on('change', function()
	{
		if ($(this).val() != "")
		{
			verificationFlags.mentor.sectionDone = true;
		}
		else
		{
			verificationFlags.mentor.sectionDone = true;
		}
	});

		 /* SCRIPT TO OPEN THE MODAL WITH THE PREVIEW */
      $("#id_avatar").change(function () {
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


	$('#submit-btn').on('click', function()
	{
		verifySection(verificationFlags.professional_info);
		var good = true;
		var errorMsg = "<ul>";
		if (mentorNeeded)
		{
			console.log("MENTOR");
			if (!verificationFlags.mentor.sectionDone)
			{
				good = false;
				errorMsg += "<li><p>" + verificationFlags.mentor.message + "</p></li>";
			}
		}

		if ($("#acaProf tr.acaRow").length == 0)
		{
			good = false;
			errorMsg += "<li><p>" + verificationFlags.degrees.message + "</p></li>";
		}

		if (verificationFlags.topics.counter == 0)
		{
			good = false;
			errorMsg += "<li><p>" + verificationFlags.topics.message + "</p></li>";
		}

		if (!verificationFlags.professional_info.sectionDone)
		{
			console.log("PROF");
			console.log(verificationFlags.professional_info.elems);
			good = false;
			if (!verificationFlags.professional_info.elems.address.done)
			{
				errorMsg += "<li><p>" + verificationFlags.professional_info.elems.address.message + "</p></li>";
			}
			if (!verificationFlags.professional_info.elems.city.done)
			{
				errorMsg += "<li><p>" + verificationFlags.professional_info.elems.city.message + "</p></li>";
			}
			if (!verificationFlags.professional_info.elems.zip.done)
			{
				errorMsg += "<li><p>" + verificationFlags.professional_info.elems.zip.message + "</p></li>";
			}
		}

		if (!verificationFlags.terms.sectionDone)
		{
			console.log("TERMS");
			good = false;
			errorMsg += "<li><p>" + verificationFlags.terms.elems.checkbox.message + "</p></li>";
		}

		if (good)
		{
			$("form").submit();
		}
		else
		{
			UIkit.modal.alert(errorMsg + "</ul>");
		}
	});
});










