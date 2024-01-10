# urls.py
from django.urls import path


from .views import UserRegistrationAPIView, UserLoginAPIView, CreateQuizAPIView

urlpatterns = [
    path('api/register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('create_quiz/', CreateQuizAPIView.as_view(), name='create-quiz'),
]
