from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager, RegularUserManager, SuperUserManager

from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(blank=True, default="", unique=True)
    name = models.CharField(max_length=255, blank=True, default="")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]


class RegularUser(User):
    objects = RegularUserManager()

    class Meta:
        proxy = True
        verbose_name = "Regular User"
        verbose_name_plural = "Regular Users"


class SuperUser(User):
    objects = SuperUserManager()

    class Meta:
        proxy = True
        verbose_name = "Super User"
        verbose_name_plural = "Super Users"



# Permission, Permission Category and Role models

# Created abstract model for common fields
class AbstractFields(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)


class PermissionCategory(AbstractFields):
    class Meta:
        verbose_name = "Permission Category"
        verbose_name_plural = "Permission Categories"

    def __str__(self):
        return f"{self.name} permission category"


class Permission(AbstractFields):
    code_name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        PermissionCategory, on_delete=models.CASCADE, related_name="permissions"
    )

    def __str__(self):
        return f"{self.category.name}'s -> {self.name}"


class Role(AbstractFields):
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name="roles"
    )

    def __str__(self):
        return self.name
