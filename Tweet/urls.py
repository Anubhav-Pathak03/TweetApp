"""
URL configuration for Tweet_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from.import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('',views.index,name='index'),
    path('',views.tweet_list,name="tweet_list"),
    path('create/',views.tweet_create,name="tweet_create"),
    path('<int:tweet_id>/delete/',views.tweet_delete,name="tweet_delete"),
    path('<int:tweet_id>/edit/',views.tweet_edit,name="tweet_edit"),
    path('register/',views.register,name="register"),
    path('like/<int:tweet_id>/', views.like_tweet, name='like_tweet'),
    path('tweet/<int:tweet_id>/comments/', views.tweet_comments_view, name='tweet_comments'),


] 