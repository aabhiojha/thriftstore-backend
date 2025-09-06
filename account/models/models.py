from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from ..managers import CustomUserManager, RegularUserManager, SuperUserManager
from .permission_models import Role, Permission, PermissionCategory

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

    roles = models.ManyToManyField(Role, blank=True, related_name="users")
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]
    
    def has_permission(self, permission_code):
        if self.is_superuser:
            return True
        qs = self.roles.filter(
            permissions__code_name = permission_code,
            permissions_is_active = True,
            is_active = True
        )
        return qs.exists()
    
    def get_all_permissions(self):
        if self.is_superuser:
            return Permission.objects.all()
        qs = Permission.objects.filter(
            roles__in=self.roles.filter(is_active=True),
            is_active=True
            ).distinct()
        return qs

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


