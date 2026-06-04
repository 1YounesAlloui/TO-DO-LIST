from django.urls import path
from . import views

urlpatterns = [
    # Application Web Pages
    path('', views.home, name='home'),
    path('tasks/', views.task_list, name='task-list'),
    path('todos/', views.todo_list, name='todo-list'),
    path('calendar/', views.calendar, name='calendar'),
    path('page/<int:task_id>/', views.page_editor, name='page-editor'),
    
    # AI Intelligence Engine
    path('ai/', views.AI, name='ai-dashboard'),
    path('api/ai/chat/', views.api_ai_chat, name='api_ai_chat'),
    path('api/ai/models/', views.api_model_list, name='api_model_list'),

    # Task Management Core CRUD API
    path('api/tasks/', views.task_list_create, name='task-list-create'),
    path('api/tasks/<int:pk>/', views.task_detail, name='task-detail'),

    # Document Cloud Storage Persistence Engine
    path('api/page/<int:task_id>/save/', views.save_document, name='save-document'),

    # Analytical Productivity Dashboard Streams
    path('api/stats/status/', views.api_stats_status, name='api-stats-status'),
    path('api/stats/daily/', views.api_stats_daily, name='api-stats-daily'),
    path('api/stats/priority/', views.api_stats_priority, name='api-stats-priority'),
    
    # Server-side Export Engines
    path('export/pdf/', views.export_pdf, name='export-pdf'),
    path('export/word/', views.export_word, name='export-word'),
]