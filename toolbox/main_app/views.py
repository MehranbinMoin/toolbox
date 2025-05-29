from django.shortcuts import render
from django.http import HttpResponse

class Tool:
    def __init__(self, name, brand, description):
        self.name = name
        self.brand = brand
        self.description = description

tools = [
    Tool('Wrench', 'Stanley', 'A wrench is a tool used to tighten or loosen bolts, nuts, and other fasteners.'),
    Tool('Screwdriver', 'Stanley', 'A screwdriver is a tool used to tighten or loosen screws.'),
    Tool('Hammer', 'Stanley', 'A hammer is a tool used to drive nails into wood.'),
]

def tools_index(request):
    return render(request, 'tools/index.html', {'tools': tools})

def home(request):
    return HttpResponse('<h1>toolbox</h1>')

def about(request):
    return render(request, 'about.html') 

def tools_simple (request):
    return HttpResponse('<h1>All available tools</h1>')

