# todos/admin.py

from django.contrib import admin
from .models import CustomerUser, Todo

admin.site.register(CustomerUser)
admin.site.register(Todo)