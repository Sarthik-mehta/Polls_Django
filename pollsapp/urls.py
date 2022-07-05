from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('vote/<str:pk>',views.vote, name='vote'),
    path('result/<str:pk>',views.result, name='result'),
    path('create',views.create, name='create'),
    path('profile',views.profile, name='profile'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),

]