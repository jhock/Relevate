/**
	* Script for dealing with contributor's degree and certification information.
 */


var universitySearchUrl;

$(document).ready(function () {
	academicId = 0;
	certId = 0;
	academicTable = [];
	certificationTable = [];
	// Stores a list of the degrees this contributor has that require
	// a mentor. If this list is empty then the mentor box does not need
	// to be shown. Otherwise, it should stay shown independent of the 
	// degree selector.
	mentorDegreeIds = [];

	$("#id_degree").change(function()
	{
		var sel = document.getElementById("id_degree");
		// 1 corresponds to the ID of the first item in degrees
		// table
		console.log("id degree changed");
		var degree = sel.options[sel.value - 9].innerHTML;
		if (degree === "Student-Undergraduate" || degree === "Student-Masters")
		{
			mentorNeeded = true;
			$('#adviser-div').removeClass('uk-hidden');
		}
		else if (mentorDegreeIds.length == 0 && !($("#adviser-div").hasClass("uk-hidden")))
		{
			mentorNeeded = false;
			$("#adviser-div").addClass('uk-hidden');
		}
	});
	// starts querying the database when user types more than one word
	$("#id_institution").keyup(function() {
			//clearTimeout($.data(this, 'timer'));
			// Retrieve the input field text and reset the count to zero
			var filter = $("#id_institution").val();
			if(filter.length > 1){
				findUniversity(filter);
				if ($('#list_of_uni').length > 0){
					$('#list_of_uni').show(1000);
					console.log("show already");
				}
			}
			else{
				$("#list_of_uni").hide()
			}
	});
});
// queries the database end point hook for school names.
function findUniversity(query_word){
	$.ajaxSetup({
			data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
		});
	var val = {
		query_word: query_word // query for 'jones'
	};
	$.ajax({
		url:universitySearchUrl,
		type: "GET",
		data: val,
		success: function(data) {
			$("#items_to_search").empty();
				  var res_data = JSON.parse(data);
				  console.log(res_data);
			for(var item = 0; item < res_data.universities.length; item++){
				var name = res_data.universities[item];
				var valid_form = name.replace("'", "’");
				$("#items_to_search").append("<li id='uni_name'><a target=\""+valid_form+"\" onclick='selectUni(\""+valid_form+"\")'>" +
						"<span class='blue'>" +
						""+name+"</span></a></li>");


			}
		},
		error: function(xhr)
		{
			// $("#error-message").text(xhr.responseText).show();
			console.log("ERROR: " + xhr.responseText);
		}
	});
}
// selects the university for the users when user clicks it from a drop down list.
function selectUni(uni_value) {
	var uni_value = uni_value;
	$("#id_institution").text(uni_value);
	$("#id_institution").val(uni_value);
	console.log(uni_value + " I am getting uni val");
	$("a[target='"+uni_value+"']").hide(1000);
	$('#list_of_uni').hide(1000);
}