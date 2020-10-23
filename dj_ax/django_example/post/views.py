import asyncio
import datetime
import time
import snap7
import random
from typing import List

import httpx
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.urls import reverse

from django.shortcuts import render
from .models import Post, Like
from django.http import HttpResponse, HttpResponseRedirect
import json

counter_task = asyncio.Task

def index(request):
    print('post index')
    posts = Post.objects.all()
    likes = Like.objects.count()
    #hello_world.delay()
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
        time.sleep(5)   # Hard work simulation
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
        time.sleep(5)   #  # Hard work simulation
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Request method is not a POST")


def button_ajax_get(request):
    if request.method == 'GET':
        print('GET')
        get_data = request.GET['text']
        back_data = list(get_data)
        random.shuffle(back_data)
        back_data = ''.join(back_data).capitalize()
        print(back_data)
        data = {
                'backtext': back_data
        }
        #time.sleep(5)   # Hard work simulation
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Request method is not a GET")


def button_ajax_post(request):
    if request.method == 'POST':
        print('POST')
        response = json.loads(request.body.decode("utf-8"))

        print(response['text'])
        back_data = list(response['text'])
        random.shuffle(back_data)
        back_data = ''.join(back_data).capitalize()
        print(back_data)
        data = {
            'backtext': back_data,
        }
        #time.sleep(5)   #  # Hard work simulation
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Request method is not a POST")

# ---------------------------------------------------------
# helpers
async def http_call_async():
    for num in range(1, 6):
        await asyncio.sleep(1)
        print(num)
    async with httpx.AsyncClient() as client:
        r = await client.get("https://httpbin.org/")
        print(r)


def http_call_sync():
    for num in range(1, 6):
        time.sleep(1)
        print(num)
    r = httpx.get("https://httpbin.org/")
    print(r)


def plc_get_data():
    plc = snap7.client.Client()
    plc.connect('192.168.0.101', 0, 1)

    byte_array = plc.db_read(151, 0, 100)
    print('\nGet byte array: ', byte_array, end='\n')

    random_float = random.uniform(0, 999)
    print(f'set new float: {random_float}')

    text = list(snap7.util.get_string(byte_array, 0, 25))
    random.shuffle(text)
    random_text = ''.join(text)
    print(f'set new text: {random_text}')

    snap7.util.set_real(byte_array, 80, random_float)
    snap7.util.set_string(byte_array, 0, random_text, 25)

    plc.db_write(152, 0, byte_array)

# views
#async def index(request):
#    return HttpResponse("Hello, async Django!")

async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())

    return HttpResponseRedirect(reverse('index'))
    #return HttpResponse("Non-blocking HTTP request")

def sync_view(request):
    http_call_sync()
    return HttpResponseRedirect(reverse('index'))
    #return HttpResponse("Blocking HTTP request")


async def smoke(smokables: List[str] = None, flavor: str = "Sweet Baby Ray's") -> None:
    """ Smokes some meats and applies the Sweet Baby Ray's """
    if smokables is None:
        smokables = [
            "ribs",
            "brisket",
            "lemon chicken",
            "salmon",
            "bison sirloin",
            "sausage",
        ]
    if (loved_smokable := smokables[0]) == "ribs":
        loved_smokable = "meats"
    for smokable in smokables:
        print(f"Smoking some {smokable}....")
        await asyncio.sleep(1)
        print(f"Applying the {flavor}....")
        await asyncio.sleep(1)
        print(f"{smokable.capitalize()} smoked.")
    print(f"Who doesn't love smoked {loved_smokable}?")


async def smoke_some_meats(request) -> HttpResponse:
    """
    http://localhost:8000/smoke_some_meats?to_smoke=ice cream, bananas, cheese&flavor=Gold Bond Medicated Powder
    """
    loop = asyncio.get_event_loop()
    smoke_args = []
    if to_smoke := request.GET.get("to_smoke"):
        # Grab smokables
        to_smoke = to_smoke.split(",")
        smoke_args += [[smokable.lower().strip() for smokable in to_smoke]]
        # Do some string prettification
        if (smoke_list_len := len(to_smoke)) == 2:
            to_smoke = " and ".join(to_smoke)
        elif smoke_list_len > 2:
            to_smoke[-1] = f"and {to_smoke[-1]}"
            to_smoke = ", ".join(to_smoke)
    else:
        to_smoke = "meats"
    if flavor := request.GET.get("flavor"):
        smoke_args.append(flavor)
    loop.create_task(smoke(*smoke_args))
    return HttpResponse(f"Smoking some {to_smoke}....")


async def async_with_sync_view(request):
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(http_call_sync)
    loop.create_task(async_function())
    return HttpResponseRedirect(reverse('index'))
    #return HttpResponse("Non-blocking HTTP request (via sync_to_async)")


async def plc_get(request):
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(plc_get_data)
    loop.create_task(async_function())
    return HttpResponseRedirect(reverse('index'))

# ---------------------------------------------------------

async def run_periodically(wait_time, func, *args):
    """
    Helper for schedule_task_periodically.
    Wraps a function in a coroutine that will run the
    given function indefinitely
    :param wait_time: seconds to wait between iterations of func
    :param func: the function that will be run
    :param args: any args that need to be provided to func
    """
    while True:
        func(*args)
        await asyncio.sleep(wait_time)

def schedule_task_periodically(wait_time, func, *args):
    """
    Schedule a function to run periodically as an asyncio.Task
    :param wait_time: interval (in seconds)
    :param func: the function that will be run
    :param args: any args needed to be provided to func
    :return: an asyncio Task that has been scheduled to run
    """
    return asyncio.create_task(run_periodically(wait_time, func, *args))

async def cancel_scheduled_task(task):
    """
    Gracefully cancels a task
    :type task: asyncio.Task
    """
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


def count_seconds_since(then):
    """
    Prints the number of seconds that have passed since then
    :type then: datetime.datetime
    :param then: Time to count seconds from
    """

    now = datetime.datetime.now()
    print(f"{(now - then).seconds} seconds have passed.")



async def main():
    print('main')
    global counter_task
    counter_task = schedule_task_periodically(3, count_seconds_since, datetime.datetime.now())
    print(counter_task, type(counter_task))
    print("Doing something..")
    await asyncio.sleep(10)
    print("Doing something else..")
    await asyncio.sleep(5)
    print("Shutting down now...")

    await cancel_scheduled_task(counter_task)
    print("Done")


async def async_main(request):
    #asyncio.get_event_loop().run_until_complete(main())
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    return HttpResponseRedirect(reverse('index'))

def async_stop(request):
    cancel_scheduled_task(counter_task)
    return HttpResponseRedirect(reverse('index'))