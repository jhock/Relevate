$(document).ready(function()
{

	$('#submit_btn').on('click', function()
	{
		verificationFlags = {
			num_advisees: {
				done: verify_num_advisees(),
				message: "Number of mentees must be a number between 0 and 255."
			},
			reason: {
				done: verify_reason(),
				message: "Must supply a reason."
			},
			terms: {
				done: $('#id_accept_terms').prop('checked'),
				message: "You must accept the terms and conditions."
			}
		}

		var good = true;
		var errorMsg = "<ul>";

		if (!verificationFlags.num_advisees.done)
		{
			errorMsg += "<li>" + verificationFlags.num_advisees.message + "</li>";
			good = false;
		}
		if (!verificationFlags.reason.done)
		{
			errorMsg += "<li>" + verificationFlags.reason.message + "</li>";
			good = false;
		}
		if (!verificationFlags.terms.done)
		{
			errorMsg += "<li>" + verificationFlags.terms.message + "</li>";
			good = false;
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

	function verify_num_advisees()
	{
		var val = $("#id_number_of_advisees").val();
		try
		{
			var num = parseInt(val);
			return 0 < num && num < 255;
		}
		catch(err)
		{
			return false;
		}
	}

	function verify_reason(){
		/**
		 * Checks to make sure reason input is valid
		 * @type {Number}
	     */
		var count = CKEDITOR.instances['id_reason'].getData().length;
		return count > 0;
	}
});