from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class SuperUserManager(CustomUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=True)


class RegularUserManager(CustomUserManager):

    def get_queryset(self):
        return super().get_queryset().filter(is_superuser=False)


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
