import json as j
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Count, Case, BooleanField, Value, When
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Dislike, Follow
from .forms import  PostForm, SignUpForm, UserForm

# TODO
# async create_post
# async edit_post

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
            num_likes=Count('like'),
            num_dislikes=Count('dislike'),
        ).order_by("-id")
    else:
        posts = Post.objects.annotate(
            num_likes=Count('like'),
            num_dislikes=Count('dislike')
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
            num_likes=Count('like'),
            num_dislikes=Count('dislike')
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
            num_likes=Count('like'),
            num_dislikes=Count('dislike')
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
def create_post(request): # not async
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
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
            # return HttpResponseRedirect(reverse("index"))
            # new_post.objects.annotate(num_likes=Count('like'))
            # return HttpResponse(render_to_string("network/post.html", {"post": new_post}))
            previous_url = request.META.get('HTTP_REFERER')

            return redirect(previous_url)
    else:
        return render(request, "network/create_post.html", {
            "form": form
        })


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


# @login_required
# def create_post(request):
#     # new_post = request.POST['body'] # works, don't lose this

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
#             except IntegrityError as e:
#                 messages.error(request, f"{e.__cause__}")
#                 return HttpResponseRedirect(reverse("index"))
#             else:
#                 messages.error(request, f"Invalid submission")
#         print(new_post)
#         # n = serializers.serialize('json', [new_post])
#         n = model_to_dict(new_post)
#         r = JsonResponse(n, status=201)
#         return r

#     else:
#         messages.error(request, f"Must be POST")
#         return redirect("index")


# @login_required
# def edit_post(request, postid): # async
#     post = Post.objects.get(id=postid)

#     if request.method == "POST":
#         post_body_edit = request.Post['body']
#         form = PostForm(initial={"body": post_body_edit})

#         if form.is_valid(): # and post.author == request.user:
#             try:
#                 post.body = form.cleaned_data["post_body_edit"]
#                 post.edited = timezone.now()
#                 post.save(update_fields=["body", "edited"])

#                 edited_post = Post.objects.get(id=post.id)
#                 j = JsonResponse({"post_body_edit": edited_post.body, "post_edited": edited_post.edited})
#                 print(j)
#                 return j

#             except IntegrityError as e:
#                 messages.error(request, f"{e.__cause__}")
#                 return redirect("index")
#         else:
#             messages.error(request, f"Invalid submission")
#             return redirect("index")
#     else:
#         messages.error(request, f"Invalid submission")
#         return redirect("index")


# @login_required # not async
# def edit_post(request, postid):
#     post = Post.objects.get(id=postid)
#     form = PostForm(initial={"body": post.body})

#     if request.method == "POST":
#         form = PostForm(request.POST)

#         if form.is_valid() and post.author == request.user:
#             try:
#                 post.body = form.cleaned_data["body"]
#                 post.edited = timezone.now()
#                 post.save(update_fields=["body", "edited"])
#                 messages.success(request, "Your post is updated!")
#             except IntegrityError as e:
#                 messages.error(request, f"{e.__cause__}")
#             return HttpResponseRedirect(reverse("index"))
#         else:
#             messages.error(request, f"Invalid submission")

#     return render(request, "network/edit_post.html", {
#         "postid": postid,
#         "form": form
#     })


@csrf_exempt
@login_required # async
def edit_post(request, postid):
    post = Post.objects.get(id=postid)
    form = PostForm(initial={"body": post.body})

    if request.method == "POST":
        form = PostForm(request.POST)
        fv = True if form.is_valid() else False
        pr = True if post.author == request.user else False
        if fv and pr:
            try:
                post.body = form.cleaned_data["body"]
                post.edited = timezone.now()
                post.save(update_fields=["body", "edited"])
                h1 = HttpResponse(render_to_string("network/post.html", {"post": post}))
                print(h1)
                return h1
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
                print(f"{e.__cause__}")
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, f"Invalid submission")
            print(f"fv: {fv}, pr: {pr}")
            return HttpResponseRedirect(reverse("index"))

    h = HttpResponse(render_to_string("network/edit_post.html", {
        "post": post,
        "postid": postid,
        "form": form
        }))
    print(h)
    return h


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
        messages.error(request, "You can't delete this post.")
    return redirect('index')


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
        redirect("index")

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
        redirect("index")

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
        redirect('index')

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
