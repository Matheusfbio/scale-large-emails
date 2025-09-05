import re
from django.utils.timezone import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from email_analyzer.forms import LogMessageForm, EmailMessageForm
from email_analyzer.models import LogMessage, EmailMessage
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .nlp_processor import EmailProcessor
import json

def home(request):
    """Renders the home page with project presentation."""
    return render(request, "email_analyzer/home.html")

def about(request):
    return render(request, "email_analyzer/about.html")

# Add this code elsewhere in the file:
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "email_analyzer/log_message.html", {"form": form})

def email_processor(request):
    """Main view for email processing"""
    if request.method == "POST":
        form = EmailMessageForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            
            # Process email using NLP
            processor = EmailProcessor()
            results = processor.process_email(
                email.subject, 
                email.content, 
                email.sender
            )
            
            # Update email with results
            email.category = results['category']
            email.confidence_score = results['confidence_score']
            email.suggested_response = results['suggested_response']
            email.is_processed = True
            email.save()
            
            return render(request, "email_analyzer/email_result.html", {
                "email": email,
                "results": results
            })
    else:
        form = EmailMessageForm()
    
    return render(request, "email_analyzer/email_processor.html", {"form": form})

def email_list(request):
    """View to list all processed emails"""
    emails = EmailMessage.objects.all()
    return render(request, "email_analyzer/email_list.html", {"emails": emails})

@csrf_exempt
def api_process_email(request):
    """API endpoint for email processing"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subject = data.get('subject', '')
            content = data.get('content', '')
            sender = data.get('sender', '')
            
            if not all([subject, content, sender]):
                return JsonResponse({
                    'error': 'Missing required fields'
                }, status=400)
            
            # Process email
            processor = EmailProcessor()
            results = processor.process_email(subject, content, sender)
            
            # Save to database
            email = EmailMessage.objects.create(
                subject=subject,
                content=content,
                sender=sender,
                category=results['category'],
                confidence_score=results['confidence_score'],
                suggested_response=results['suggested_response'],
                is_processed=True
            )
            
            return JsonResponse({
                'id': email.id,
                'category': results['category'],
                'confidence_score': results['confidence_score'],
                'suggested_response': results['suggested_response'],
                'is_productive': results['is_productive']
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'error': 'Method not allowed'
    }, status=405)

def email_analytics(request):
    """View for email analytics and statistics"""
    total_emails = EmailMessage.objects.count()
    productive_emails = EmailMessage.objects.filter(category='produtivo').count()
    unproductive_emails = EmailMessage.objects.filter(category='improdutivo').count()
    
    if total_emails > 0:
        productive_percentage = (productive_emails / total_emails) * 100
        unproductive_percentage = (unproductive_emails / total_emails) * 100
    else:
        productive_percentage = 0
        unproductive_percentage = 0
    
    # Get recent emails
    recent_emails = EmailMessage.objects.order_by('-received_date')[:10]
    for email in recent_emails:
      email.confidence_display = round(email.confidence_score * 100, 1)


    context = {
        'total_emails': total_emails,
        'productive_emails': productive_emails,
        'unproductive_emails': unproductive_emails,
        'productive_percentage': round(productive_percentage, 1),
        'unproductive_percentage': round(unproductive_percentage, 1),
        'recent_emails': recent_emails
    }
    
    return render(request, "email_analyzer/email_analytics.html", context)
