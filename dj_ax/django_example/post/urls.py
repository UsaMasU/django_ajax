from django.urls import path
from .views import (
    index, likePost_get,
    likePost_post,
    button_ajax_get,
    button_ajax_post,
    async_view, sync_view,
    smoke_some_meats,
    async_with_sync_view,
    async_main, async_stop, plc_get
)

urlpatterns = [
    path('', index, name='index'),
    path('button_ajax_get/', button_ajax_get, name='button_ajax_get'),
    path('button_ajax_post/', button_ajax_post, name='button_ajax_post'),
    path('likepost_get/', likePost_get, name='likepost_get'),
    path('likepost_post/', likePost_post, name='likepost_post'),
    path("async/", async_view),
    path("sync/", sync_view),
    path("smoke_some_meats/", smoke_some_meats),
    path("sync_to_async/", async_with_sync_view),
    path("async_main/", async_main),
    path("async_stop/", async_stop),
    path("plc/", plc_get),
   ]

