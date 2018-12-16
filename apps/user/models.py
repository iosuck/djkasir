from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, level, username, password):
        if not username:
            raise TypeError('Error boy')

        user = self.model(
            level=level,
            username=username,
        )
        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, level, username, password):
        user = self.create_user(
            level=level,
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    status = (
        ('1', 'Super Admin'),
        ('2', 'Admin'),
        ('3', 'User'),
    )
    level = models.CharField(max_length=10, choices=status, default=3)
    username = models.CharField(max_length=255, unique=True)
    nama = models.CharField(max_length=255)
    telp = models.CharField(max_length=100, blank=True, null=True)
    alamat = models.TextField("alamat", blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['level']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def is_staff(self):
        return True
