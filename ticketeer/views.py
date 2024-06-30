from ticketeer.models import TicketeerTask
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .serializers import RegisterSerializer, TaskSerializer, TaskStatusSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied


class LoginView(ObtainAuthToken):
    """
    Custom login view to authenticate users and generate tokens.
    Inherits:
        ObtainAuthToken: Base class to obtain authentication tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate users.
        Args:
            request: HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: JSON response containing authentication token and user details.
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class RegisterView(generics.CreateAPIView):
    """
    View for user registration.
    Attributes:
        serializer_class: Serializer class for user registration.
        permission_classes: Permissions required for accessing this view (none for registration).
    """

    serializer_class = RegisterSerializer
    permission_classes = []  # No authentication necessary for registration

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.
        Args:
            request: HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        Returns:
            Response: JSON response indicating success or failure of registration.
        """
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Registration successful'}, status=response.status_code)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    """
    View for listing and creating tasks.
    Attributes:
        serializer_class: Serializer class for tasks.
        permission_classes: Permissions required for accessing this view (authenticated users only).
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of tasks for the authenticated user.
        Returns:
            QuerySet: Filtered queryset of tasks.
        """
        return TicketeerTask.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        """
        Save the new task with the authenticated user as the author.
        Args:
            serializer: Serializer instance for the task being created.
        """
        serializer.save(author=self.request.user)


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting tasks.
    Attributes:
        serializer_class: Serializer class for tasks.
        permission_classes: Permissions required for accessing this view (authenticated users only).
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the queryset of tasks for the authenticated user.
        Returns:
            QuerySet: Filtered queryset of tasks.
        """
        return TicketeerTask.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        """
        Perform update operation on a task instance.
        Args:
            serializer: Serializer instance for the task being updated.
        Raises:
            PermissionDenied: If the current user is not the author of the task.
        """
        instance = serializer.save()
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this task")

    def perform_destroy(self, instance):
        """
        Perform delete operation on a task instance.
        Args:
            instance: Task instance to be deleted.
        Raises:
            PermissionDenied: If the current user is not the author of the task.
        """
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this task")
        instance.delete()


class TaskStatusUpdateAPIView(generics.UpdateAPIView):
    """
    View for updating the status of a task.
    Attributes:
        queryset: Queryset of all tasks.
        serializer_class: Serializer class for tasks.
        permission_classes: Permissions required for accessing this view (authenticated users only).
    """

    queryset = TicketeerTask.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests to update the status of a task.
        Args:
            request: HTTP request object.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response indicating success or failure of status update.
        """
        instance = self.get_object()
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to update this task")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    """
    API endpoint for creating a new task.
    Args:
        request: HTTP request object containing task data.
    Returns:
        Response: JSON response indicating success or failure of task creation.
    """
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)