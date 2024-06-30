# serializers.py
from ticketeer.models import TicketeerTask
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.
    Handles the validation and creation of a new User instance.
    Attributes:
        password: A write-only field for the user's password.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Create and return a new User instance.
        Args:
            validated_data (dict): Validated data containing user information.
        Returns:
            User: The newly created User instance.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
    
    
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task objects.
    Serializes Task model instances to JSON representation.
    Attributes:
        author: The author of the task. Automatically populated and read-only.
    """

    class Meta:
        model = TicketeerTask
        fields = '__all__'
        read_only_fields = ('author',)


class TaskStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Task status.
    Handles partial updates of Task status.
    Attributes:
        status: The updated status of the Task.
    """
    class Meta:
        model = TicketeerTask
        fields = ['status']
