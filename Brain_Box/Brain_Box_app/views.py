from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .serializers import UserSerializer, UserLoginSerializer, QuizSerializer
from .models import CustomToken


class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create a token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = CustomToken.objects.get_or_create(user=user)

        # Update the expiration time to 1 hour from now
        token.expiration_time = timezone.now() + timezone.timedelta(hours=1)
        token.save()

        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)


class CreateQuizAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
