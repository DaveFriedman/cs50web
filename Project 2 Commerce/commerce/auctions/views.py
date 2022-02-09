from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *

"""
TODO
bids
comments
tighten up login redirects
html/css styling
message alerts colors
Create form?
"""


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True).order_by("-id")
    })


def read_category(request, category):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(
            is_active=True, category=category).order_by("-id")
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            try:
                new_listing = Listing.objects.create(
                    name = form.cleaned_data["name"],
                    category = form.cleaned_data["category"],
                    description = form.cleaned_data["description"],
                    image_url = form.cleaned_data["image_url"],
                    list_price = form.cleaned_data["list_price"],
                    is_active = True,
                    lister = User.objects.get(pk=request.user.id)
                )
                new_listing.save()

                if new_listing.id is not None:
                    try:
                        bid = Bid.objects.create(
                            bid_price = form.cleaned_data["list_price"],
                            bid_time = datetime.now(),
                            bidder = new_listing.lister,
                            listing = new_listing
                        )
                        bid.save()
                    except IntegrityError as e:
                        messages.error(request, f"{e.__cause__}")
                        return render(request, "auctions/create_listing.html", {
                            "form": form,
                        })
                messages.success(request, f"Your {new_listing.name} is listed!")
                return HttpResponseRedirect(reverse("read", kwargs={
                    "id": new_listing.id, 
                    "name": new_listing.name,
                }))
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
                return render(request, "auctions/create_listing.html", {
                    "form": form,
                })
        else:
            messages.error(request, f"There was an error with this submission.")
            return render(request, "auctions/create_listing.html", {
                "form": form,
            })
    else:
        return render(request, "auctions/create_listing.html", {
        "form": ListingForm(),
    })


def read_listing(request, id, name):
    listing = Listing.objects.get(id=id)
    listing.category = listing.get_category_display()

    if listing.is_active == False:
        messages.error(request, "Sorry, this listing was closed.")
        return HttpResponseRedirect(reverse("index"))

    owner = False
    watched = False
    if request.user.is_authenticated:
        user = request.user
        if listing.lister == user:
            owner = True
        if Watchlist.objects.filter(user=user, listing=listing).exists():
            watched = True

    bids = Bid.objects.filter(listing=id).order_by("-bid_time")
    comments = Comment.objects.filter(listing=id).order_by("-commented")

    return render(request, "auctions/read_listing.html", {
        "owner": owner,
        "watched": watched,
        "listing": listing,
        "bids": bids,
        "comments": comments
    })


@login_required
def close_listing(request, id, name):
    listing = Listing.objects.get(id=id)
    try:
        listing.is_active = False
        listing.save()
        messages.success(request, f"Your listing of {listing.name} is closed.")        
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")

    return HttpResponseRedirect(reverse("index"))


@login_required
def read_watchlist(request):
    user = User.objects.get(id=request.user.id)
    watchlist = Watchlist.objects.filter(user=user)
    listings = Listing.objects.filter(
        watchlist__in=watchlist, is_active=True).order_by("-id")

    return render(request, "auctions/index.html", {
        "listings": listings
    })


@login_required
def watch(request, id, name):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=id)

    if Watchlist.objects.filter(user=user, listing=listing).exists():
        try:
            w = Watchlist.objects.filter(user=user, listing=listing)
            w.delete()
            messages.success(request, f"Removed from your watchlist")
        except IntegrityError as e:
            messages.error(request, f"{e.__cause__}")
    else:
        try:
            w = Watchlist.objects.create(user=user, listing=listing)
            w.save()
            messages.success(request, f"Added to your watchlist")
        except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")

    return HttpResponseRedirect(reverse("read", kwargs={
        "id": id,
        "name": name
    }))



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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
