import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.serializers import *
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Follow
from .forms import  PostForm, SignUpForm, UserForm

# TODO
# async create_post
# likes
# follows

def index(request):
    posts = Post.objects.all().order_by("-id")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/feed.html", {
        "form": PostForm(),
        "posts": page_obj
    })


@login_required
def following(request):
    user = request.user
    creators = Follow.objects.filter(follower=user).values("creator")
    posts = Post.objects.filter(author__in=creators).order_by("-id")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/feed.html", {
        "form": PostForm(),
        "posts": page_obj
    })


@login_required
def profile(request, profileid, profilename):
    profile = User.objects.get(id = profileid)
    posts = Post.objects.filter(author=profile).order_by("-id")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "form": PostForm(),
        "profile": profile,
        "follower_count": Follow.objects.filter(creator=profile).count(),
        "following_count": Follow.objects.filter(follower=profile).count(),
        "user_follows_profile": True if Follow.objects.filter(
            follower=request.user, creator=profile).exists() else False,
        "posts": page_obj
    })


# @login_required
# def create_post(request): # not async
#     form = PostForm()
#     if request.method == "POST":
#         form = PostForm(request.POST)

#         if form.is_valid():
#             try:
#                 new_post = Post.objects.create(
#                     body = form.cleaned_data["body"],
#                     author = request.user,
#                     posted = timezone.now(),
#                     edited = timezone.now()
#                 )
#                 new_post.save()
#                 messages.success(request, "Your post is up!")
#             except IntegrityError as e:
#                 messages.error(request, f"{e.__cause__}")
#             return HttpResponseRedirect(reverse("index"))
#     else:
#         return render(request, "network/create_post.html", {
#             "form": form
#         })


# @login_required
# def create_post(request): # async
#     if request.method == "POST":
#         post_body = request.POST.get("post")
#         # print("body:", post_body)
#         # [print(p) for p in post_body]
#         if post_body is None:
#             return JsonResponse({"error": "Post cannot be empty."}, status=400)

#         try:
#             new_post = Post.objects.create(
#                     body = post_body,
#                     author = request.user,
#                     posted = timezone.now(),
#                     edited = timezone.now()
#                 )
#             new_post.save()
#             return JsonResponse({"message": "Post successful."}, status=201)
#         except IntegrityError as e:
#             return JsonResponse({"error": f"{e.__cause__}"}, status=400)
#     else:
#         return JsonResponse({"error": "POST request required."}, status=400)


@csrf_exempt
@login_required
def create_post(request):

    post = Post.objects.get(id=1)
    JSONSerializer = get_serializer("json")
    json_serializer = JSONSerializer()
    json_serializer.serialize(post)
    new_post = json_serializer.getvalue()

    new_post = serialize("json", Post.objects.get(id=1))

    if request.method == "POST":
        new_post = json.loads(request.body)


        for post in deserialize("json", request.post):
            if post.is_valid(): # or something
                print(post.object)
        pass
    else:
        messages.error(request, f"Must be POST")

    return redirect("index")


@login_required
def edit_post(request, postid):
    post = Post.objects.get(id=postid)
    form = PostForm(initial={"body": post.body})

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid() and post.author==request.user:
            try:
                post.body = form.cleaned_data["body"]
                post.edited = timezone.now()
                post.save(update_fields=["body", "edited"])
                messages.success(request, "Your post is updated!")
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, f"Invalid submission")

    return render(request, "network/edit_post.html", {
        "postid": postid,
        "form": form
    })


@login_required
def read_post(request, postid):
    post = Post.objects.get(id=postid)
    return render(request, "network/feed.html", {
        "posts": [post]
    })


@login_required
def follow(request, profileid):
    follower = request.user
    creator = User.objects.get(id=profileid)

    try:
        f = Follow.objects.get(creator=creator, follower=follower)
        f.delete()
        user_follows_profile = False
    except Follow.DoesNotExist:
        f = Follow.objects.create(creator=creator, follower=follower)
        f.save()
        user_follows_profile = True
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")
        redirect('profile', profileid=creator.id, profilename=creator.username)
    return JsonResponse({"user_follows_profile": user_follows_profile})



@login_required
def account_settings(request):
    form = UserForm(instance=request.user)

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=request.user)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                messages.success(request, "Your account settings are updated!")
            except IntegrityError as e:
                messages.error(request, f"error: {e.__cause__}")
            redirect("settings")
        else:
            messages.error(request, f"Please correct the error below.s")

    return render(request, "network/account_settings.html", {
        "form": form,
        "last_login": request.user.last_login,
        "date_joined": request.user.date_joined
        })


@login_required
def change_account_password(request):
    form = PasswordChangeForm(request.user)

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, instance=request.user)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, ("Your password was updated!"))
            except IntegrityError as e:
                messages.error(request, f"error: {e.__cause__}")
            return redirect("password")
        else:
            messages.error(request, ("Please correct the error below."))

    return render(request, "network/change_account_password.html", {
        "form": form
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, ("Invalid username and/or password."))

    return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            except IntegrityError as e:
                messages.error(request, f"error: {e.__cause__}")

    return render(request, "network/register.html", {
        "form": form
    })
