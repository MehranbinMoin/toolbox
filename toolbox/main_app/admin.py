from django.contrib import admin
from .models import Tool, Reservation, Comment

admin.site.register(Tool)
admin.site.register(Reservation)
admin.site.register(Comment)