from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    # print(request.POST['page'])
    return HttpResponse("{\"key\":\"Hello,世界.Hello, python\"}", content_type="application/json,charset=utf-8")
