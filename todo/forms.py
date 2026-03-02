from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Todo,CustomerUser

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomerUser.ROLE_CHOICE)

    class Meta:
        model = CustomerUser
        fields = ['username','role','password1','password2']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','descriptions','completed']