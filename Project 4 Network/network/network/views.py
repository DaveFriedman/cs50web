from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Count, Case, BooleanField, Value, When
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.formats import localize
import json

from .models import User, Post, Like, Dislike, Follow
from .forms import  PostForm, SignUpForm, UserForm


def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.annotate(
            user_likes=Case(
                When(like__liker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            user_dislikes=Case(
                When(dislike__disliker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            num_likes=Count("like"),
            num_dislikes=Count("dislike"),
        ).order_by("-id")
    else:
        posts = Post.objects.annotate(
            num_likes=Count("like"),
            num_dislikes=Count("dislike")
            ).order_by("-id")

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

    posts = Post.objects.filter(author__in=creators
        ).annotate(
            user_likes=Case(
                When(like__liker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            user_dislikes=Case(
                When(dislike__disliker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            num_likes=Count("like"),
            num_dislikes=Count("dislike")
        ).order_by("-id")

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

    posts = Post.objects.filter(author=profile
        ).annotate(
            user_likes=Case(
                When(like__liker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            user_dislikes=Case(
                When(dislike__disliker=request.user, then=Value(True)),
                default=Value(False),
                output_field=BooleanField()
            ),
            num_likes=Count("like"),
            num_dislikes=Count("dislike")
        ).order_by("-id")

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "form": PostForm(),
        "profile": profile,
        "follower_count": Follow.objects.filter(creator=profile).count(),
        "following_count": Follow.objects.filter(follower=profile).count(),
        "is_follower": True if Follow.objects.filter(
            follower=request.user, creator=profile).exists() else False,
        "posts": page_obj
    })


@login_required
def create_post(request):
    form = PostForm()

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            try:
                new_post = Post.objects.create(
                    body = form.cleaned_data["body"],
                    author = request.user,
                    posted = timezone.now(),
                    edited = timezone.now()
                )
                new_post.save()
                messages.success(request, "Your post is up!")

                return redirect(request.META.get("HTTP_REFERER"))

            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")

    return render(request, "network/create_post.html", {
        "form": form
    })


@login_required
def edit_post(request, postid):
    post = Post.objects.get(id=postid)
    # form = PostForm(initial={"body": post.body})

    if request.method == "POST":
        post_body_update = json.loads(request.body)
        if post.author == request.user:
            try:
                post.body = post_body_update
                post.edited = timezone.now()
                post.save(update_fields=["body", "edited"])

                updated_post = Post.objects.get(id=postid)
                return JsonResponse({
                    "postid": updated_post.id,
                    "postbody": updated_post.body,
                    "postedited": localize(updated_post.edited, "DATETIME_FORMAT")
                    }, status=201)

            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
        messages.error(request, f"Invalid submission")

    return redirect(request.META.get("HTTP_REFERER"))
    # return render(request, "network/edit_post.html", {
    #     "post": post,
    #     "postid": postid,
    #     "form": form
    #     })


@login_required
def delete_post(request, postid):
    post = Post.objects.get(id=postid)

    if post.author == request.user:
        try:
            post.delete()
            messages.success(request, "Your post was deleted.")
        except IntegrityError as e:
            messages.error(request, f"{e.__cause__}")
    else:
        messages.error(request, "You cannot delete this post.")

    return redirect(request.META.get("HTTP_REFERER"))



@login_required
def read_post(request, postid):
    post = Post.objects.get(id=postid)
    return render(request, "network/feed.html", {
        "posts": [post]
    })


@login_required
def like_post(request, postid):
    liker = request.user
    post = Post.objects.get(id=postid)

    try:
        l = Like.objects.get(liker=liker, post=post)
        l.delete()
        is_liker = False
    except Like.DoesNotExist:
        l = Like.objects.create(liker=liker, post=post)
        l.save()
        is_liker = True
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")
        return redirect(request.META.get("HTTP_REFERER"))


    like_count = Like.objects.filter(post=post).count()
    return JsonResponse({"is_liker": is_liker, "like_count": like_count})


@login_required
def dislike_post(request, postid):
    disliker = request.user
    post = Post.objects.get(id=postid)

    try:
        l = Dislike.objects.get(disliker=disliker, post=post)
        l.delete()
        is_disliker = False
    except Dislike.DoesNotExist:
        l = Dislike.objects.create(disliker=disliker, post=post)
        l.save()
        is_disliker = True
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")
        return redirect(request.META.get("HTTP_REFERER"))


    dislike_count = Dislike.objects.filter(post=post).count()
    return JsonResponse({"is_disliker": is_disliker, "dislike_count": dislike_count})


@login_required
def follow(request, profileid):
    follower = request.user
    creator = User.objects.get(id=profileid)

    try:
        f = Follow.objects.get(creator=creator, follower=follower)
        f.delete()
        is_follower = False
    except Follow.DoesNotExist:
        f = Follow.objects.create(creator=creator, follower=follower)
        f.save()
        is_follower = True
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")
        return redirect(request.META.get("HTTP_REFERER"))

    follower_count = Follow.objects.filter(creator=creator).count()
    return JsonResponse({"is_follower": is_follower, "follower_count": follower_count})


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

                return redirect("settings")

            except IntegrityError as e:
                messages.error(request, f"error: {e.__cause__}")
        else:
            messages.error(request, f"Please correct the error below.")

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

                return redirect("password")

            except IntegrityError as e:
                messages.error(request, f"error: {e.__cause__}")
        else:
            messages.error(request, f"Please correct the error below.")

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
            origin = request.META.get("HTTP_ORIGIN")
            referer = request.META.get("HTTP_REFERER")
            tail = referer.find("/login?next=") + 12 # len("/login?next=")=12
            print("origin ", origin, "referer ", referer, "tail ", tail)
            if tail == 11: #11 = 12-1, where "-1" is referer.find() not found
                return redirect("index")
            else:
                destination = origin + referer[tail:]
                return redirect(destination)
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
