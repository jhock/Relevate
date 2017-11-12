$('#link-form').submit(function(event)
{
	$('#load-icon').removeClass('invisible');
});

var charCap = "/400";
$(document).ready(function()
{
	$('char-count').text("0" + charCap);
});