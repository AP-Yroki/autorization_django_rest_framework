from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.status import HTTP_200_OK

from .models import Class, Student, Subject, User
from .serializer import ClassSerializer, UserRegistrSerializer, UserLoginSerializer, SubjectSerializer, StudentSerializer
from rest_framework.permissions import (IsAuthenticated, IsAdminUser, AllowAny,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.authtoken.models import Token
from .permissions import IsAdminOrReadonly
from rest_framework.response import Response
from django.contrib.auth import logout
# Create your views here.

class ClassList(ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]


class ClassUpdate(RetrieveUpdateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAdminUser]


class ClassDestroy(RetrieveDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SubjectList(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class SubjectseUpdate(RetrieveUpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadonly]


class SubjectDestroy(RetrieveDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadonly]

class StudentList(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]


class StudentUpdate(RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadonly]


class StudentDestroy(RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrReadonly]

class RegistrUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)

            data['data'] = serializer.data
            data['user_token'] = token.key
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)

class LoginUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request: WSGIRequest, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return JsonResponse({
                'error': {
                    'code': 401,
                    'message': 'Authenticated failed'
                }
            })
        user = serializer.validated_data
        print('good', user)
        if user:
            token_object, token_created = Token.objects.get_or_create(user=user)
            token = token_object if token_object else token_created

            return Response({'user_token': token.key}, status=HTTP_200_OK)
        return Response({'error': {'message': 'Authentication failed'}})

class LogOutUserView(ListAPIView):
    def get(self, request: WSGIRequest, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            return JsonResponse({
                'error': {
                    'code': 401,
                    'message': 'Logout failed'
                }
            }, status=401)

        logout(request)