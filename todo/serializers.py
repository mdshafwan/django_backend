# todo/serializers.py

from rest_framework import serializers
from .models import Todo

class todoerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'completed', 'created_at']