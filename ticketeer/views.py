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
    def post(self, request, *args, **kwargs):
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
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Registration successful'}, status=response.status_code)

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketeerTask.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TicketeerTask.objects.filter(author=self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to edit this task")

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("You do not have permission to delete this task")
        instance.delete()
    
class TaskStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = TicketeerTask.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
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
    data = request.data
    data['author'] = request.user.id

    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)