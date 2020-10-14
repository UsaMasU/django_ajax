from django.urls import path
from .views import index, likePost_get, likePost_post


urlpatterns = [
    path('', index, name='index'),
    path('likepost_get/', likePost_get, name='likepost_get'),
    path('likepost_post/', likePost_post, name='likepost_post'),
   ]

