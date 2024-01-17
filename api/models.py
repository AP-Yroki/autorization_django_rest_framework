from django.contrib.auth.models import AbstractUser, BaseUserManager, \
    PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            **extra_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, username, password):
        return self._create_user(email, username, password)

    def create_superuser(self, email, username, password):
        return self._create_user(email, username, password, is_staff=True,
                                 is_superuser=True)


class User(AbstractUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.email


class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Student(models.Model):
    full_name = models.CharField(max_length=50)
    age = models.IntegerField()
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grades = models.IntegerField()

    def __str__(self):
        return self.full_name


class Class(models.Model):
    name = models.CharField(max_length=10, default='5Б')
    year_of_study = models.IntegerField()
    students = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name