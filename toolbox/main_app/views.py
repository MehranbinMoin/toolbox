from django.shortcuts import render
from .models import Tool

def tools_index(request):
    tools = Tool.objects.all()
    return render(request, 'tools/index.html', {'tools': tools})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html') 

def tool_detail(request, tool_id):
    tool = Tool.objects.get(id=tool_id)
    return render(request, 'tools/detail.html', {'tool': tool})


