from rest_framework.views import APIView
from ..serializer.feed_serializer import PostSerializer
from rest_framework.response import Response
from ...contribution.models.post_model import Post


class FeedView(APIView):
	'''
		@TODO Rest Api View for grabbing post feed
	'''
	def get(self, request, feed_index, format=None):
		all_posts = Post.objects.all().order_by('publishedDate')
		index = int(feed_index)
		if index > 0:
			next_posts = all_posts[index:index+30]
		else:
			next_posts = all_posts[:30]
		serializer = PostSerializer(next_posts, many=True)
		return Response(serializer.data)




