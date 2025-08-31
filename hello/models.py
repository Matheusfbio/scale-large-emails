from django.db import models
from django.utils import timezone

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class EmailMessage(models.Model):
    CATEGORY_CHOICES = [
        ('produtivo', 'Produtivo'),
        ('improdutivo', 'Improdutivo'),
    ]
    
    subject = models.CharField(max_length=200)
    content = models.TextField()
    sender = models.CharField(max_length=100)
    received_date = models.DateTimeField("date received", default=timezone.now)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    confidence_score = models.FloatField(default=0.0)
    suggested_response = models.TextField(blank=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Email from {self.sender}: {self.subject}"
    
    class Meta:
        ordering = ['-received_date']
