from django.urls import path
from . import views



app_name = 'accounts'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view()),
	path('activation/<int:user_id>/', views.UserActivationView.as_view()),
]