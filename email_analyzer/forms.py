from django import forms
from email_analyzer.models import LogMessage, EmailMessage

class LogMessageForm(forms.ModelForm):
    """Form for the log message model."""
    class Meta:
        model = LogMessage
        fields = ("message",)

class EmailMessageForm(forms.ModelForm):
    """Form for email message processing."""
    class Meta:
        model = EmailMessage
        fields = ['subject', 'content', 'sender']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assunto do email'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Conteúdo do email...'
            }),
            'sender': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Remetente'
            })
        }
        labels = {
            'subject': 'Assunto',
            'content': 'Conteúdo',
            'sender': 'Remetente'
        }
