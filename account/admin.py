from django.contrib import admin
from .models import RegularUser, SuperUser, User


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        return super().save_model(request, obj, form, change)


#
# admin.site.register(User, UserAdmin)


@admin.register(RegularUser)
class RegularUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=False)


@admin.register(SuperUser)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_superuser=True)
