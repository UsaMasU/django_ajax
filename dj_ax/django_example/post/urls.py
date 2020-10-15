from django.urls import path
from .views import index, likePost_get, likePost_post, button_ajax_get, button_ajax_post


urlpatterns = [
    path('', index, name='index'),
    path('button_ajax_get/', button_ajax_get, name='button_ajax_get'),
    path('button_ajax_post/', button_ajax_post, name='button_ajax_post'),
    path('likepost_get/', likePost_get, name='likepost_get'),
    path('likepost_post/', likePost_post, name='likepost_post'),
   ]

