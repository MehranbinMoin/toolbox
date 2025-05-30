from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('tools/', views.tools_index, name='tools-index'),
    path('tools/<int:tool_id>/', views.tool_detail, name='tool-detail'),
    path('tools/create/', views.ToolCreate.as_view(), name='tool-create'),
    path('tools/<int:pk>/update/', views.ToolUpdate.as_view(), name='tool-update'),
    path('tools/<int:pk>/delete/', views.ToolDelete.as_view(), name='tool-delete'),
]
