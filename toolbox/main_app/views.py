from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>toolbox</h1>')

def about(request):
    return render(request, 'about.html') 

def tools (request):
    return HttpResponse('<h1>All available tools</h1>')

