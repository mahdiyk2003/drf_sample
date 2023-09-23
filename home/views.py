from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post,Comment,Like
from .serializers import PostSerializer,CommentSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from permissions import IsTheAuthorOrIsAdminOrReadOnly,IsAnAuthorOrIsAnAdminOrReadOnly
from django.shortcuts import get_object_or_404
class MainPageView(APIView):
	permission_classes=[IsAuthenticated,]
	def get(self , request):
		posts=Post.objects.filter(is_activate=True)
		ser_data=PostSerializer(instance=posts,many=True)
		return Response(data=ser_data.data,status=status.HTTP_200_OK)

class PostCreateView(APIView):
	permission_classes=[IsAnAuthorOrIsAnAdminOrReadOnly,]

	def post(self,request):
		ser_data = PostSerializer(data=request.data)
		if ser_data.is_valid():
			post=ser_data.create(ser_data.validated_data,request.user)
			return Response(data={'message':'created successfully'}, status=status.HTTP_201_CREATED)
		return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

class PostView(APIView):
	permission_classes=[IsTheAuthorOrIsAdminOrReadOnly]
	def setup(self, request, *args, **kwargs):
		self.post=get_object_or_404(Post,pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)

	def get(self,request,post_id):
		ser_data = PostSerializer(instance=self.post)
		return Response(data=ser_data.data)


	def delete(self,request,post_id):
		self.post.delete()
		return Response(data={'message':'post deleted successfully'}, status=status.HTTP_202_ACCEPTED)

	def put(self,request,post_id):
		self.check_object_permissions(request,obj=self.post)

		ser_data=PostSerializer(instance=self.post,data=request.POST,partial=True)
		if ser_data.is_valid():
			ser_data.save()
			return Response(data={'message':'post updated successfully'})
		return Response(data=ser_data.errors)


class PostActivationView(APIView):
	permission_classes=[IsTheAuthorOrIsAdminOrReadOnly]

	def setup(self, request, *args, **kwargs):
		self.post=get_object_or_404(Post,pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)
	def get(self,request,post_id):
		if not self.post.is_active:
			self.post.is_active = True
			self.post.save()
			return Response({'message':'post activated'},status=status.HTTP_202_ACCEPTED)
		return Response({'post is already activated.'},status=status.HTTP_400_BAD_REQUEST)

	def delete(self,request,post_id):
		if self.post.is_active:
			self.post.is_active = False
			self.post.save()
			return Response({'message':'post deactivated'},status=status.HTTP_202_ACCEPTED)
		return Response({'post is already deactivated.'},status=status.HTTP_400_BAD_REQUEST)



class PostAddCommentView(APIView):
	permission_classes=[IsAuthenticated,]

	def post(self,request,post_id):
		post=get_object_or_404(Post,pk=post_id)
		ser_data = CommentSerializer(data=request.data)
		if ser_data.is_valid():
			comment=ser_data.create(ser_data.validated_data,request.user,post)
			return Response(data={'message':'created successfully'}, status=status.HTTP_201_CREATED)
		return Response(ser_data.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class PostLikeView(APIView):
	permission_classes=[IsAuthenticated]

	def setup(self, request, *args, **kwargs):
		self.post=get_object_or_404(Post,pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)


	def get(self,request,post_id):
		if self.post.user_can_like(request.user):
			Like(user=request.user,post=self.post).save()
			return Response({'message':'user liked the post successfully'},status=status.HTTP_202_ACCEPTED)
		return Response({'user has already liked the post.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

	def delete(self,request,post_id):
		if not self.post.user_can_like(request.user):
			Like.objects.get(user==request.user,post=self.post).delete()
			return Response({'message':'user unliked the post successfully'},status=status.HTTP_202_ACCEPTED)
		return Response({"user hasn't liked the post,So the user can't unlike it"}, status=status.HTTP_406_NOT_ACCEPTABLE)