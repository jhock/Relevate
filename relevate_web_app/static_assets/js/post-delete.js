function confirmDeletion()
{
	var message = "Are you sure you want to delete this article?";
	if(confirm(message)){
		removeArticle();
	}
}

function removeArticle()
{
	/**
	 * Ajax call for removing a post object based on the post id.
	 */
	$.ajaxSetup({
		data: {csrfmiddlewaretoken: '{{ csrf_token }}'}
	});
	var slug_var = '{{ post.slug }}';
	$.ajax({
		url: "{% url 'contribution:post_remove' %}",
		type: "POST",
		data: { slug: slug_var },
		success: function(data)
		{
			var res_data = JSON.parse(data);
			if (res_data.deleted == true){
				window.location.replace("{% url 'contribution:all_posts' %}");
			}
			else{
				$("#error-message").show();
				console.log("something went wrong" + res_data.deleted);
			}
		},
		error: function(xhr)
		{
			// $("#error-message").text(xhr.responseText).show();
			$("#error-message").show();
			console.log("ERROR: " + xhr.responseText);
		}
	})
}