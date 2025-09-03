from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("log/", views.log_message, name="log_message"),
    path("email/", views.email_processor, name="email_processor"),
    path("email/list/", views.email_list, name="email_list"),
    path("email/analytics/", views.email_analytics, name="email_analytics"),
    path("api/email/process/", views.api_process_email, name="api_process_email"),
]

