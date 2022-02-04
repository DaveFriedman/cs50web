from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import models, forms
# from .models import User, Listing, Bid, Comment
# from .forms import ListingForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "form": forms.CategoryForm(),
        "listings": models.Listing.objects.all()
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = forms.ListingForm(request.POST)

        if form.is_valid():
            try:
                new_listing = models.Listing.objects.create(
                    name = form.cleaned_data["name"],
                    category = form.cleaned_data["category"],
                    description = form.cleaned_data["description"],
                    image_url = form.cleaned_data["image_url"],
                    list_price = form.cleaned_data["list_price"],

                    is_active = True,
                    lister = models.User.objects.get(pk=request.user.id)
                )
                new_listing.save()

                if new_listing.id is not None:
                    try:
                        bid = models.Bid.objects.create(
                            bid_price = form.cleaned_data["list_price"],
                            bid_time = datetime.now(),

                            bidder = new_listing.lister,
                            listing = new_listing
                        )
                        bid.save()

                    except IntegrityError as e:
                        messages.error(request, f"{e.__cause__}")
                        return render(request, "auctions/create_listing.html", {
                            "form": form})          

                messages.success(request, f"Your {new_listing.name} is listed!")
                return HttpResponseRedirect(reverse("read", kwargs={
                    "id": new_listing.id, 
                    "name": new_listing.name
                    }))
            
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
                return render(request, "auctions/create_listing.html", {
                    "form": form})

        else:
            # messages.error(request, f"Your submission has errors:") #form.errors
            return render(request, "auctions/create_listing.html", {
                "form": form
            })

    else:
        return render(request, "auctions/create_listing.html", {
            "form": forms.ListingForm()
        })


def read_listing(request, id, name):
    listing = models.Listing.objects.get(id=id)
    listing.category = listing.get_category_display()
    bids = models.Bid.objects.filter(listing=id).order_by("-bid_time")
    comments = models.Comment.objects.filter(listing=id).order_by("-commented")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments
    })


def read_category(request, category):
    # if request.method == "POST":
    if forms.CatagoryForm(request.GET):
        form = forms.CategoryForm(request.GET)
        if form.is_valid():
            category = form.cleaned_data["category"]
            # if category == '('',)':
            #     return HttpResponseRedirect(reverse("index"))

            return render(request, "auctions/index.html", {
                "cat": category,
                "form": forms.CategoryForm(),
                "listings": models.Listing.objects.filter(category='category')
            })

    else:
        return HttpResponseRedirect(reverse("index"))


# @login_required
# def update_listing(request):
#     # https://dev.to/sankalpjonna/save-your-django-models-using-updatefields-for-better-performance-50ig
#     pass


# @login_required
# def delete_listing(request):
#     pass


def random(request):
    pass


def search(request):
    pass


def watchlist(request):
    pass


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = models.User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
