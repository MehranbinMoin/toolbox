from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User 
from cloudinary.models import CloudinaryField

class Tool(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    # image = CloudinaryField('image')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tool-detail', kwargs={'tool_id': self.id})
    
class ToolPhoto(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('image')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"Photo for {self.tool.name}"    

class Reservation(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tool.name} reserved by {self.user.username}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username}."