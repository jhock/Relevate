'''
@TODO The serializers for Rest Api Calls for Mobile Device
'''
#query all post data based on time. Get top 40
#send a json representation to the client side
from django.contrib.auth.models import User
from ...contribution.models.post_model import Post
from ...contribution.models.article_model import Article
from ...contribution.models.infographic_model import Infographic
from ...contribution.models.link_model import Link
from ...contribution.models.topic_model import Topics
from rest_framework import serializers


class TopicSerializer(serializers.ModelSerializer):

	class Meta:
		model = Topics
		fields = ('name', 'description')


class LinkSerializer(serializers.ModelSerializer):
	topics = TopicSerializer(read_only=True, many=True)

	class Meta:
		model = Link
		fields = ('topics', 'title', 'url', 'description', 'image')


class InfographicSerializer(serializers.ModelSerializer):
	topics = TopicSerializer(read_only=True, many=True)

	class Meta:
		model = Infographic
		fields = ('title', 'image', 'topics', 'is_image', 'thumbnail')


class ArticleSerializer(serializers.ModelSerializer):

	article_topics = TopicSerializer(read_only=True, many=True)
	class Meta:
		model = Article
		fields = ('article_topics', 'image', 'title', 'content', 'blurb')


class PostSerializer(serializers.ModelSerializer):
	infographic = InfographicSerializer(read_only=True)
	article = ArticleSerializer(read_only=True)
	link = LinkSerializer(read_only=True)

	class Meta:
		model = Post
		fields = ('is_article', 'is_link', 'is_infographic', 'article', 'infographic', 'likes', 'views',
				  'createdDate', 'link')





