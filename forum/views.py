from django.shortcuts import render
from django.http import HttpResponse
from .models import ForumUser, Post


def index(request):

	return HttpResponse("I'll fix this later.")
