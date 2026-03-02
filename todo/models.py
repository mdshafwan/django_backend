from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    ROLE_CHOICE = (('admin','ADMIN'),('student','STUDENT'))
    role = models.CharField(max_length=10,choices=ROLE_CHOICE,default="student")

class Todo(models.Model):
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    title = models.TextField(max_length=10)
    descriptions = models.TextField(max_length=200)
    completed= models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title   