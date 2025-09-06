from django.db import models

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
