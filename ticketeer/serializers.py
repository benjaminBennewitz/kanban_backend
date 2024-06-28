# serializers.py
from ticketeer.models import TicketeerTask
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    
    
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketeerTask
        fields = '__all__'
        read_only_fields = ('author',)
        
class TaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketeerTask
        fields = ['status']