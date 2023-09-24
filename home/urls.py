from django.urls import path
from . import views


app_name='home'

urlpatterns=[
    path('', views.MainPageView.as_view()),
	path('post/<int:post_id>/', views.PostView.as_view()),
	path('post/activation/<int:post_id>/', views.PostActivationView.as_view()),
	path('post/create/', views.PostCreateView.as_view()),
	path('comment/create/<int:post_id>/', views.PostAddCommentView.as_view()),
	path('comment/<int:comment_id>/', views.CommentView.as_view()),
	path('like/<int:post_id>/', views.PostLikeView.as_view()),
]