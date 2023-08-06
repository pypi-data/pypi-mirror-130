
from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from tkm.models import Post
from .serializers import *
from django.contrib.auth.models import User,Group
from rest_framework import viewsets,permissions

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import Group, Messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView


from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    GroupUpdateForm,
    GroupProfileUpdateForm,
    MessageCreateForm,
    GroupCreateForm,
    GroupProfileCreateForm,
    SearchUserForm,
    AddMemberForm
)



from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib.auth.models import User
import json
from django.utils.safestring import mark_safe




@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Post.objects.all()
        serializer = MySerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)





@csrf_exempt
def snippet_detail(request, pk):
 
    try:
        snippet = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MySerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MySerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)






