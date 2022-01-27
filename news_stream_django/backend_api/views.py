import json

from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from backend_api.models import SocialPost


def index(request):
    posts = SocialPost.objects.limit(5)
    data = []
    for p in posts:
        p = json.loads((p.to_json()))
        data.append(p)
    return JsonResponse(data, safe=False)
    # return HttpResponse("Hello, world. You're at the polls index.")