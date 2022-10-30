"""URL Patternd of the Accounts"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.dashboard, name = "dashboard"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.register, name = "register"),
    path("edit/", views.edit, name = "edit"),
    path("user/",views.user_list, name = "user_list"),
    path("users/<username>/", views.user_detail, name = "user_detail"),
    path("users/follow/", views.user_follow, name = "user_follow"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
