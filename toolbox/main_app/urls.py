from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tools/', views.tools_index, name='tools-index'),
    path('tools/<int:tool_id>/', views.tool_detail, name='tool-detail')
]
