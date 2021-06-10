
from django.urls import path
from accounts.views import UserRegistration

app_name = "accounts"
urlpatterns = [
    path('registration/', UserRegistration.as_view(), name='registration')
]