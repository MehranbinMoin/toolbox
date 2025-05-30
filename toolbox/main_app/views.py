from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tool, Reservation
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.forms.models import model_to_dict
from .forms import ReservationForm, CommentForm

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
    tool = get_object_or_404(Tool, id=tool_id)
    reservations_with_comments = tool.reservations.prefetch_related('comments__author').all()
    
    context = {
        'tool': tool,
        'reservations_with_comments': reservations_with_comments,
        'reservation_form': ReservationForm(),
    }
    return render(request, 'tools/detail.html', context)

@login_required
def add_reservation(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.tool = tool
            reservation.user = request.user
            reservation.save()
            return redirect('tool-detail', tool_id=tool.id)
    return redirect('tool-detail', tool_id=tool.id)

@login_required
def add_comment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.reservation = reservation
            comment.save()
            return redirect('tool-detail', tool_id=reservation.tool.id)
    return redirect('tool-detail', tool_id=reservation.tool.id)