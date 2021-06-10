from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

class UserRegistration(CreateView):
    form_class = UserCreationForm
    template_name = "form.html"
    success_url = "/polls/"