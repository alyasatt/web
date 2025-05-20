# echo/admin.py
from django.contrib import admin
from .models import CustomUser, Book

# Регистрация модели CustomUser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'user_role', 'is_active', 'is_admin', 'is_staff', 'last_login', 'date_joined')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('user_role', 'is_active', 'is_admin', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)

# Регистрация модели Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'price')
    search_fields = ('name', 'author')
    list_filter = ('author',)

admin.site.register(Book, BookAdmin)
