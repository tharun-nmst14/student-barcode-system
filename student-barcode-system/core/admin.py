from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser

from django.contrib import admin
from .models import Student  # 👈 Import your model

@admin.register(Student)  # 👈 Register the model
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'roll_number', 'email']  # Customize this as needed


# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ['username', 'email', 'role', 'is_staff']

# admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
