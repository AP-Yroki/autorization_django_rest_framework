from django.contrib.auth import authenticate
from django.contrib.auth.models import AbstractUser

from .models import Class, User, Subject, Student
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
class UserRegistrSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Пароль не совпадает'})

        user.set_password(password)
        user.save()

        # После сохранения пользователя создаем токен
        token = Token.objects.create(user=user)

        return user
class UserLoginSerializer(serializers.Serializer):
    user: User = None
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        return False

