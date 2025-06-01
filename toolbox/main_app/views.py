from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tool, Reservation, Comment, ToolPhoto 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.models import model_to_dict
from django.contrib import messages
from .forms import ReservationForm, CommentForm
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class ToolCreate(LoginRequiredMixin, CreateView):
    model = Tool
    fields = '__all__'

    def form_valid(self, form):
        form.instance.owner = self.request.user  
        return super().form_valid(form)
    
@login_required
def add_photos(request, tool_id):
    tool = get_object_or_404(Tool, id=tool_id, owner=request.user)
    
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        for i, image in enumerate(images):
            caption = request.POST.get(f'caption_{i}', '')
            ToolPhoto.objects.create(
                tool=tool,
                image=image,
                caption=caption,
                order=i
            )
        return redirect('tool-detail', tool_id=tool.id)
    
    return render(request, 'tools/add_photos.html', {'tool': tool})

@login_required
def delete_photo(request, photo_id):
    photo = get_object_or_404(ToolPhoto, id=photo_id, tool__owner=request.user)
    tool_id = photo.tool.id
    photo.delete()
    return redirect('tool-detail', tool_id=tool_id)   

class ToolUpdate(LoginRequiredMixin,UpdateView):
    model = Tool
    fields = '__all__'

    def get_queryset(self):
        return Tool.objects.filter(owner=self.request.user)

class ToolDelete(LoginRequiredMixin,DeleteView):
    model = Tool
    success_url = '/tools/'

    def get_queryset(self):
        return Tool.objects.filter(owner=self.request.user)

@login_required
def tools_index(request):
    tools = Tool.objects.all()
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        tools = tools.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        ).distinct()
    tools = tools.order_by('-is_available', 'name')
    
    context = {
        'tools': tools,
        'search_query': search_query,
    }
    
    return render(request, 'tools/index.html', context)

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')

@login_required
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

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        messages.error(request, "You can only edit your own reservations.")
        return redirect('tool-detail', tool_id=reservation.tool.id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservation updated successfully!")
            return redirect('tool-detail', tool_id=reservation.tool.id)
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
        'tool': reservation.tool,
    }
    return render(request, 'reservations/edit.html', context)

@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if reservation.user != request.user:
        messages.error(request, "You can only delete your own reservations.")
        return redirect('tool-detail', tool_id=reservation.tool.id)
    
    tool_id = reservation.tool.id
    
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, "Reservation deleted successfully!")
        return redirect('tool-detail', tool_id=tool_id)
    
    context = {
        'reservation': reservation,
        'tool': reservation.tool,
    }
    return render(request, 'reservations/confirm_delete.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        messages.error(request, "You can only edit your own comments.")
        return redirect('tool-detail', tool_id=comment.reservation.tool.id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('tool-detail', tool_id=comment.reservation.tool.id)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'reservation': comment.reservation,
        'tool': comment.reservation.tool,
    }
    return render(request, 'comments/edit.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if comment.author != request.user:
        messages.error(request, "You can only delete your own comments.")
        return redirect('tool-detail', tool_id=comment.reservation.tool.id)
    
    tool_id = comment.reservation.tool.id
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('tool-detail', tool_id=tool_id)
    
    context = {
        'comment': comment,
        'reservation': comment.reservation,
        'tool': comment.reservation.tool,
    }
    return render(request, 'comments/confirm_delete.html', context)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tools-index')
        else:
            error_message = 'Invalid sign up - please try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
  
