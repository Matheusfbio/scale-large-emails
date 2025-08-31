from django.contrib import admin
from hello.models import LogMessage, EmailMessage

@admin.register(LogMessage)
class LogMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'log_date')
    list_filter = ('log_date',)
    search_fields = ('message',)

@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'subject', 'category', 'confidence_score', 'received_date', 'is_processed')
    list_filter = ('category', 'is_processed', 'received_date')
    search_fields = ('sender', 'subject', 'content')
    readonly_fields = ('received_date', 'confidence_score', 'suggested_response')
    
    fieldsets = (
        ('Informações do Email', {
            'fields': ('sender', 'subject', 'content', 'received_date')
        }),
        ('Análise da IA', {
            'fields': ('category', 'confidence_score', 'suggested_response', 'is_processed')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-received_date')
