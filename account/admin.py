from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        return super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
