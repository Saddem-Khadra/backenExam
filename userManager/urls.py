from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('user', views.UserView.as_view(), name='user'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('notfriends', views.NotFriendsView.as_view(), name='notfriends'),

]
