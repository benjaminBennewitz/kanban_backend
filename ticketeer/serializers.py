from rest_framework import serializers
from ticketeer.models import TodoItem

class TodoItemSerialzer(serializers.ModelSerializer):
    class Meta:
        model = TodoItem
        fields = '__all__'