from rest_framework import serializers
from .models import Post,Comment,Like
from django.utils.text import slugify



class PostSerializer(serializers.ModelSerializer):
	comments=serializers.SerializerMethodField(read_only=True,required=False)
	likes=serializers.SerializerMethodField(read_only=True,required=False)
	likes_count=serializers.SerializerMethodField(read_only=True,required=False)
	class Meta:
		model = Post
		exclude=['is_active','slug']
		extra_kwargs = {
			'created': {'read_only':True},
			'updated': {'read_only':True},
			'user': {'required':False},
		}
	def create(self, validated_data,user):
		post=Post(user=user,body=validated_data['body']
					,slug=slugify(validated_data['body'][:30]),title=validated_data['title'])
		post.save()
		return post

	def get_likes(self,obj):
		return LikeSerializer(instance=obj.plikes.all() , many=True).data

	def get_likes_count(self,obj):
		return obj.likes_count()


	def get_comments(self,obj):
		return CommentSerializer(instance=obj.pcomments.all() , many=True).data


class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Comment
		fields='__all__'
	extra_kwargs = {
			'created': {'read_only':True},
			'user': {'read_only':True},
			'post': {'read_only':True},
		}

	def create(self, validated_data,user,post):
		comment=Comment(user=user,post=post,body=validated_data['body'])
		comment.save()
		return post

class LikeSerializer(serializers.ModelSerializer):
	class Meta:
		model=Like
		fields='__all__'
	extra_kwargs = {
			'created': {'read_only':True},
			'user': {'read_only':True},
			'post': {'read_only':True},
		}
	
	def create(self, validated_data,user,post):
		like=Like(user=user,post=post)
		like.save()
		return post