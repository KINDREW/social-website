"""Registering models for Admin"""
from django.contrib import admin
from .models import Image
# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Adding Image model to Admin Site"""
    list_display = ("title","slug", "image","created")
    list_filter = ["created"]
