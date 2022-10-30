"""Views for the accounts"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from actions.models import Actions
from bookmarks.common.decorators import ajax_required
from .forms import LoginForm, UserRegistrationForm,UserEditForm,ProfileEditForm
from .models import Profile, Contact
from actions.utils import create_action
# Create your views here.
def user_login(request):
    """Creating the user login view"""
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request,username = clean_data['username'],
            password = clean_data["password"])
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return HttpResponse("Authenticated successfully")
                else:
                    return HttpResponse("Disabled Account")
            else:
                return HttpResponse("Invalid Login")
    else:
        form = LoginForm()
    return render(request,"account/login.html",{"form":form})
@login_required
def dashboard(request):
    """User, after login"""
    actions = Actions.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list("id", flat="true")
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions =actions.select_related("user","user__profile").prefetch_related("target")[:10]
    return render(request, "account/dashboard.html",{"section":"dashboard","actions":actions})

def register(request):
    """User registers view"""
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password2"])
            new_user.save()
            Profile.objects.create(user = new_user)
            create_action(new_user,"has created an account")
            return render(request, 'account/register_done.html',{"new_user":new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})

@login_required
def edit(request):
    """Letting user edit their profile"""
    if request.method =="POST":
        user_form = UserEditForm(instance=request.user,data = request.POST)
        profile_form = ProfileEditForm(instance= request.user.profile,
        data = request.POST, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "profile Updated Successfully")
        else:
            messages.error(request, "Error updating your profile")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, "account/edit.html", {"user_form": user_form,
    "profile_form":profile_form})

@login_required
def user_list(request):
    """Getting the user list"""
    users = User.objects.filter(is_active =True)
    return render(request, "account/user/list.html", {"section":"people","users":users})

@login_required
def user_detail(request, username):
    """Getting user detial view"""
    user = get_object_or_404(User,username = username,  is_active =True)
    return render(request,"account/user/detail.html", {"section":"people","user":user})

@ajax_required
@require_POST
@login_required
def user_follow(request):
    """Letting users follow each other"""
    user_id = request.POST.get("id")
    action = request.POST.get("action")
    if user_id and action:
        try:
            user = User.objects.get(id = user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user,
                user_to=request.user)
                create_action(request.user, "is following", user)
            else:
                Contact.objects.filter(user_from=request.user,
                user_to=user).delete()
                return JsonResponse({"status":"ok"})
        except User.DoesNotExist:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})
