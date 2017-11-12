function addSession(id)
	/*
		Adds button to selected expertise topic section. Terrible Name!
		@TODO change name of function without breaking anything else.
	*/
{
	$("#"+id).css('visibility', 'hidden');
	var name = $("#"+id).text();

	$('[value='+id+']').prop('checked', true).trigger('change');
	var str = createButton(id, name);
	$("#chosen-item-list").append(str);
}

function createButton(id, name)
{
	/**
		Creates a button html element that looks like this

		<div id="remove1" class='uk-width-1-3 uk-margin-small'>
			<button class="topic-btn uk-button uk-button primary" type="button" onclick="removeItem('1');" value=1>
				<span class="uk-icon-check">Breaking Up</span>
			</button>
		</div>

	*/
	console.log('button created');
	var str = '<div id="remove' + id + '" class="uk-width-1-3 uk-margin-small">' +
				'<button class="already-selected uk-button uk-button-primary" ' +
						'type="button" onclick="removeItem('+id+');" value='+id+'>'+
					'<span class="uk-icon-check">' + name + '</span>' +
				'</button>' +
			'</div>';

	return str;
}

function removeItem(id)
{
	/**
		Remove button item for expertise topic upon clicking of that button.
	*/
	//console.log("Removing " + id);
	$("#remove"+id).remove();
	$('[value='+id+']').prop('checked', false).trigger('change');
	$("#"+id).css('visibility', 'visible');
	$("#"+id).removeAttr('hidden');

}













