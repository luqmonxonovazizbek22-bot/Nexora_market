from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone


class Contact(models.Model):
    name = models.CharField()
    phone_number = models.CharField()
    subject = models.CharField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    img = models.ImageField()
    title = models.CharField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField()
    author = models.CharField()

    def __str__(self):
        return self.title



class Product(models.Model):
    img = models.ImageField()
    title = models.CharField()

    review = models.IntegerField(default=0)

    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    old_price = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.CharField()

    def __str__(self):
        return self.title


# ---------------------------------------------------------- Auth



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email (gmail) kiritilishi shart")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email