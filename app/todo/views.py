import json
import os
import requests
from datetime import timedelta

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from dotenv import load_dotenv


from .models import Task

load_dotenv()

# ------------------- Load system prompt -------------------
SYSTEM_PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'system_prompt.txt')
try:
    with open(SYSTEM_PROMPT_PATH, 'r', encoding='utf-8') as f:
        BASE_SYSTEM_PROMPT = f.read().strip()
except FileNotFoundError:
    BASE_SYSTEM_PROMPT = (
        "You are a highly professional AI assistant. "
        "Respond in a structured, insightful manner using Markdown formatting."
    )

# Mode-specific additions
MODE_PROMPTS = {
    'summarize': '\n\nYour task is to create an executive summary of the following content. Highlight key points, actions, and outcomes.',
    'humanize': '\n\nYour task is to rewrite the following text to sound natural, conversational, and professional while preserving meaning.',
}

# ------------------- Pages --------------------
def home(request):
    return render(request, 'home.html')

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks.html', {'tasks': tasks})

def todo_list(request):
    return render(request, 'to_do_list/todo_list.html')

def calendar(request):
    return render(request, 'to_do_list/calendar.html')

def page_editor(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'page.html', {'task': task})

def AI(request):
    return render(request, 'AI_assistant/AI.html')

# ------------------- Document saving -------------------
@csrf_exempt
@require_http_methods(["POST"])
def save_document(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = json.loads(request.body)
    task.content = data.get('content', '')
    task.save()
    return JsonResponse({'success': True})

# ------------------- Server-Side Document Export -------------------
@csrf_exempt
@require_http_methods(["POST"])
def export_pdf(request):
    html_content = request.POST.get('html_content', '')
    if not html_content:
        return HttpResponse("No content provided", status=400)
        
    full_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{ size: a4 portrait; margin: 2cm; }}
            body {{ font-family: Helvetica, Arial, sans-serif; font-size: 11pt; }}
            img {{ max-width: 100%; height: auto; }}
            table {{ width: 100%; border-collapse: collapse; }}
            td, th {{ border: 1px solid #ddd; padding: 8px; }}
            blockquote {{ border-left: 4px solid #ddd; padding-left: 10px; margin-left: 0; color: #555; }}
        </style>
    </head>
    <body>{html_content}</body>
    </html>
    """
    
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(full_html.encode("UTF-8")), result)
    
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Workspace_Export.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

@csrf_exempt
@require_http_methods(["POST"])
def export_word(request):
    html_content = request.POST.get('html_content', '')
    if not html_content:
        return HttpResponse("No content provided", status=400)
        
    doc_html = f"""
    <html xmlns:o='urn:schemas-microsoft-com:office:office' 
          xmlns:w='urn:schemas-microsoft-com:office:word' 
          xmlns='http://www.w3.org/TR/REC-html40'>
    <head><meta charset='utf-8'><title>Export</title></head>
    <body>{html_content}</body>
    </html>
    """
    response = HttpResponse(doc_html.encode("UTF-8"), content_type='application/msword')
    response['Content-Disposition'] = 'attachment; filename="Workspace_Export.doc"'
    return response

# ------------------- AI Model Registry -------------------
def get_model_registry():
    """Returns models available for each provider."""
    return {
        "groq": [
            {"id": "llama-3.3-70b-versatile", "label": "Llama 3.3 70B (Groq)"},
            {"id": "llama-3.1-8b-instant", "label": "Llama 3.1 8B Instant"},
            {"id": "mixtral-8x7b-32768", "label": "Mixtral 8x7B (Groq)"},
            {"id": "gemma2-9b-it", "label": "Gemma 2 9B IT"},
        ],
        "openrouter": [
            {"id": "openai/gpt-4o-mini", "label": "GPT-4o Mini"},
            {"id": "google/gemini-1.5-pro", "label": "Gemini 1.5 Pro"},
            {"id": "google/gemini-1.5-flash", "label": "Gemini 1.5 Flash"},
            {"id": "deepseek/deepseek-chat", "label": "DeepSeek V3"},
            {"id": "meta-llama/llama-3.3-70b-instruct", "label": "Llama 3.3 70B (OpenRouter)"},
        ]
    }

@csrf_exempt
def api_model_list(request):
    """Returns the list of available AI providers and models."""
    registry = get_model_registry()
    return JsonResponse(registry)

# ------------------- AI Chat Proxy -------------------
@csrf_exempt
@require_http_methods(["POST"])
def api_ai_chat(request):
    try:
        data = json.loads(request.body)
        provider = data.get('provider', 'groq')
        model = data.get('model', '')
        mode = data.get('mode', 'chat')
        prompt_text = data.get('prompt', '')

        if not prompt_text:
            return JsonResponse({'error': 'Prompt is required.'}, status=400)

        system_instruction = BASE_SYSTEM_PROMPT
        if mode in MODE_PROMPTS:
            system_instruction += MODE_PROMPTS[mode]

        # Select endpoint & headers
        if provider == 'groq':
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not set.")
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
        elif provider == 'openrouter':
            api_key = os.getenv("OPENROUTER_API_KEY")
            if not api_key:
                raise ValueError("OPENROUTER_API_KEY not set.")
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Workspace AI"
            }
        else:
            return JsonResponse({'error': 'Invalid provider'}, status=400)

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt_text}
            ],
            "temperature": 0.7,
            "max_tokens": 1000   # ← CRITICAL: respects OpenRouter free‑tier limit
        }

        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response_data = response.json()

        if response.status_code == 200:
            ai_output = response_data['choices'][0]['message']['content']
            return JsonResponse({'reply': ai_output})
        else:
            error_msg = response_data.get('error', {}).get('message', 'Upstream error')
            return JsonResponse({'error': error_msg}, status=response.status_code)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
# ------------------- Task CRUD API -------------------
@csrf_exempt
@require_http_methods(["GET", "POST"])
def task_list_create(request):
    if request.method == 'GET':
        tasks = list(Task.objects.all().values())
        return JsonResponse(tasks, safe=False)
    data = json.loads(request.body)
    task = Task.objects.create(
        title=data.get('title', ''),
        description=data.get('description', ''),
        status=data.get('status', 'pending'),
        priority=data.get('priority', 'medium'),
        due_date=data.get('due_date', None),
    )
    return JsonResponse({'id': task.id, 'title': task.title}, status=201)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'GET':
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'priority': task.priority,
            'due_date': task.due_date.isoformat() if task.due_date else None,
        })
    if request.method == 'PUT':
        data = json.loads(request.body)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        if 'due_date' in data:
            task.due_date = data['due_date']
        task.save()
        return JsonResponse({'success': True})
    task.delete()
    return JsonResponse({'success': True})

# ------------------- Statistics API -------------------
def api_stats_status(request):
    statuses = Task.Status.values
    counts = {s: Task.objects.filter(status=s).count() for s in statuses}
    return JsonResponse({
        'labels': [Task.Status(s).label for s in statuses],
        'data': [counts[s] for s in statuses],
    })

def api_stats_daily(request):
    today = timezone.now().date()
    days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    counts = [Task.objects.filter(created_at__date=day).count() for day in days]
    return JsonResponse({
        'labels': [d.strftime('%a %d') for d in days],
        'data': counts,
    })

def api_stats_priority(request):
    priorities = Task.Priority.values
    counts = {p: Task.objects.filter(priority=p).count() for p in priorities}
    return JsonResponse({
        'labels': [Task.Priority(p).label for p in priorities],
        'data': [counts[p] for p in priorities],
    })