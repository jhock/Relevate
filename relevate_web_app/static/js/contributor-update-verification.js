/**
 * Front end validation script for contributor creation.
 * Note: it puts each user's input into a dictionary with key word 'done' reflecting each
 * inputs validity.
 */

$(document).ready(function()
{
    var currentTab = 0; // Current tab is set to be the first tab (0)

    console.log("test next button function");
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
//				biography: {
//					done: $("#id_biography").val().length > 0,
//					message: "You must complete the professional interests section",
//				},
			},
		}
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
		console.log(len);
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

//	$("#id_biography").on('keyup', function()
//	{
//		var len = $(this).val().length;
//		verifyTextInput(len, 'professional_info', 'biography',
//			'#professional-info-done', '#professional-info-incomplete');
//	});

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
    console.log('test');
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
      console.log('test');
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


    function showTab(n) {
      // This function will display the specified tab of the form ...
      var x = document.getElementsByClassName("tab");
      x[n].style.display = "block";
      // ... and fix the Previous/Next buttons:
      if (n == 0) {
        document.getElementById("prevBtn_container").style.display = "none";
      } else {
        document.getElementById("prevBtn_container").style.display = "initial";
        document.getElementById("nextBtn_container").style.display = "initial";
        var nextBtn = document.getElementById("nextBtn")
        nextBtn.classList.remove('solid')
        nextBtn.classList.add('ghost')
        nextBtn.innerHTML = 'Next';
      }
      if (n == (x.length - 1)) {
        var nextBtn = document.getElementById("nextBtn")
        nextBtn.classList.remove('ghost')
        nextBtn.classList.add('solid')
        document.getElementById("nextBtn_container").style.display = "none";
      }
      // ... and run a function that displays the correct step indicator:
      fixStepIndicator(n)
    }

//    function nextPrev(n) {
    $('#prevBtn').on('click', function() {
      // scroll to the top of the page on previous
      window.scrollTo({
        top: 0
      })
      // This function will figure out which tab to display
      var x = document.getElementsByClassName("tab");
      // Exit the function if any field in the current tab is invalid:
      if (-1 == 1 && !validateForm()) return false;
      // Hide the current tab:
      x[currentTab].style.display = "none";
      // Increase or decrease the current tab by 1:
      currentTab = currentTab + -1;
      console.log(currentTab);
      // Otherwise, display the correct tab:
      showTab(currentTab);
    });

    $('#nextBtn').on('click', function() {
      console.log("next");
      window.scrollTo({
        top: 0
      })
      // This function will figure out which tab to display
      var x = document.getElementsByClassName("tab");
      // Exit the function if any field in the current tab is invalid:
      if (1 == 1 && !validateForm()) return false;
      // Hide the current tab:
      x[currentTab].style.display = "none";
      // Increase or decrease the current tab by 1:
      currentTab = currentTab + 1;
      console.log(currentTab);
      console.log(x.length);
      // Otherwise, display the correct tab:
      showTab(currentTab);
    });

    $('#submitBtn').on('click', function() {
        window.scrollTo({
        top: 0
        })
        // This function will figure out which tab to display
        var x = document.getElementsByClassName("tab");
        // Exit the function if any field in the current tab is invalid:
        if (-1 == 1 && !validateForm()) return false;
        if (confirm("Warning! All changes to User and Contributor profiles will be saved.")) {
            if (currentTab >= x.length) {
            //...the form gets submitted:
            console.log("submiting form");
            $("form").submit();

            // hide the footer
            var footer = document.getElementsByClassName('rv-contributor-form_footer')[0]
            footer.style.display = 'none'

            // display the spinner
            var container = document.getElementById('contributorApplication')
            container.classList.remove('rv-contributor-form')
            renderSpinner('contributorApplication', 'Submitting')
            }
        }
    });

    function validateForm() {
        // This function deals with validation of the form fields
        verifySection(verificationFlags.professional_info);
        var valid = true;
        var errorMsg = "<ul>";

        console.log("validating");
        //if we are on the first tab, check that fields are filled out
        if (currentTab == 0)
        {
            if (mentorNeeded)
            {
                console.log("MENTOR");
                if (!verificationFlags.mentor.sectionDone)
                {
                    valid = false;
                    errorMsg += "<li><p>" + verificationFlags.mentor.message + "</p></li>";
                }
            }
            if ($("#acaProf tr.acaRow").length == 0)
            {
                valid = false;
                console.log("first");
                errorMsg += "<li><p>" + verificationFlags.degrees.message + "</p></li>";
            }
        }

        //check second tab
        if (currentTab == 1)
        {
            if (verificationFlags.topics.counter == 0)
            {
                valid = false;
                errorMsg += "<li><p>" + verificationFlags.topics.message + "</p></li>";
            }
        }

        //check third tab
        if (currentTab == 2)
        {
            if (!verificationFlags.professional_info.sectionDone)
            {
                console.log("PROF");
                console.log(verificationFlags.professional_info.elems);
                valid = false;
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
        }

        // If the valid status is true, mark the step as finished and valid:
        if (valid) {
          document.getElementsByClassName("tab")[currentTab].className += " finish";
        }
        if (!valid) {
            UIkit.modal.alert(errorMsg + "</ul>");
        }
        console.log(valid);
        return valid; // return the valid status
    }

    function fixStepIndicator(n) {
      // This function removes the "active" class of all steps...
      var i;
      var x = document.getElementsByClassName("tab");
      for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
      }
      //... and adds the "active" class to the current step:
      x[n].className += " active";
    }

    	var frm = $("form");

        $('#save').on('click', function()
	{
	    var contributor_temp_save_url = document.getElementById("contributor_temp_save").value;
	    $('form').attr('action', contributor_temp_save_url);
	    console.log("saved");
	    $.ajaxSetup({
            data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
        });
        $.ajax({
            type: "POST",
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $("#demo").html(data);
            },
            error: function(data) {
                $("#demo").html("Something went wrong!");
            }
        });

	});

//	$('#submit-btn').on('click', function()
//	{
//		verifySection(verificationFlags.professional_info);
//		var good = true;
//		var errorMsg = "<ul>";
//
//		//if we are on the first tab, check that fields are filled out
//		if (currentTab == 0)
//        {
//            if (mentorNeeded)
//            {
//                console.log("MENTOR");
//                if (!verificationFlags.mentor.sectionDone)
//                {
//                    good = false;
//                    errorMsg += "<li><p>" + verificationFlags.mentor.message + "</p></li>";
//                }
//            }
//            if ($("#acaProf tr.acaRow").length == 0)
//            {
//                good = false;
//                errorMsg += "<li><p>" + verificationFlags.degrees.message + "</p></li>";
//            }
//        }
//
//        //check second tab
//        if (currentTab == 1)
//        {
//            if (verificationFlags.topics.counter == 0)
//            {
//                good = false;
//                errorMsg += "<li><p>" + verificationFlags.topics.message + "</p></li>";
//            }
//        }
//
//        //check third tab
//        if (currentTab == 1)
//        {
//            if (!verificationFlags.professional_info.sectionDone)
//            {
//                console.log("PROF");
//                console.log(verificationFlags.professional_info.elems);
//                good = false;
//                if (!verificationFlags.professional_info.elems.address.done)
//                {
//                    errorMsg += "<li><p>" + verificationFlags.professional_info.elems.address.message + "</p></li>";
//                }
//                if (!verificationFlags.professional_info.elems.city.done)
//                {
//                    errorMsg += "<li><p>" + verificationFlags.professional_info.elems.city.message + "</p></li>";
//                }
//                if (!verificationFlags.professional_info.elems.zip.done)
//                {
//                    errorMsg += "<li><p>" + verificationFlags.professional_info.elems.zip.message + "</p></li>";
//                }
//            }
//        }
//
//        //check fourth and final tab
//        if (currentTab == 1)
//        {
//            if (!verificationFlags.terms.sectionDone)
//            {
//                console.log("TERMS");
//                good = false;
//                errorMsg += "<li><p>" + verificationFlags.terms.elems.checkbox.message + "</p></li>";
//            }
//        }
//
//		if (good)
//		{
//			$("form").submit();
//		}
//		else
//		{
//			UIkit.modal.alert(errorMsg + "</ul>");
//		}
//	});
});










