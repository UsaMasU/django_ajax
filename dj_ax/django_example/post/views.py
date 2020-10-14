import time
from django.shortcuts import render
from .models import Post, Like
from django.http import HttpResponse
import json


def index(request):
    posts = Post.objects.all()
    likes = Like.objects.count()
    ctx = {
        'posts': posts,
        'likes': likes
    }
    return render(request, 'post/index.html', ctx)


def likePost_get(request):
    if request.method == 'GET':
        print('GET')
        post_id = request.GET['post_id']
        likedpost = Post.objects.get(pk=post_id)  # getting the liked posts
        m = Like(post=likedpost)  # Creating Like Object
        m.save()  # saving it to store in database
        likedpost_count = Like.objects.count()
        data = {
                'name': 'Ajax GET',
                'count': likedpost_count
        }
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Request method is not a GET")


def likePost_post(request):
    if request.method == 'POST':
        print('POST')
        response = json.loads(request.body.decode("utf-8"))
        print(response)
        data = {
            'name': 'Ajax POST',
            'count': Like.objects.count(),
            'fruit': response['fruit']
        }
        #time.sleep(5)
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Request method is not a POST")