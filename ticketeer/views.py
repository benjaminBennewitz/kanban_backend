from ticketeer.models import TicketeerTask
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from .serializers import RegisterSerializer, TaskSerializer, TaskStatusSerializer
from rest_framework.decorators import api_view, permission_classes


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
    queryset = TicketeerTask.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketeerTask.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
class TaskStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = TicketeerTask.objects.all()
    serializer_class = TaskStatusSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Stelle sicher, dass der Benutzer authentifiziert ist
def create_task(request):
    data = request.data
    data['author'] = request.user.id  # Setze den Autor des Tasks auf den aktuellen Benutzer

    serializer = TaskSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)