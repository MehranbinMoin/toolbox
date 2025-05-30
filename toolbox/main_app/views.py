from django.shortcuts import render
from .models import Tool
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Tool
from django.http import JsonResponse
from django.forms.models import model_to_dict

class ToolCreate(CreateView):
    model = Tool
    fields = '__all__'

class ToolUpdate(UpdateView):
    model = Tool
    fields = '__all__'

class ToolDelete(DeleteView):
    model = Tool
    success_url = '/tools/'

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


