from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .forms import *
from .utils import *

"""
TODO
fix login redirects
html/css styling
"""


def index(request):
    return render(request, "auctions/index.html", {
        "header": "Active Listings",
        "listings": Listing.objects.filter(is_active=True).order_by("-id")
    })


def read_category(request, category):
    return render(request, "auctions/index.html", {
        "header": f"Active listings in {Listing.category_displayname(category)}",
        "listings": Listing.objects.filter(is_active=True, category=category).order_by("-id")
    })


@login_required
def create_bid(request, id, name):
    if request.method == "POST":
        form = BidForm(request.POST)

        if form.is_valid():
            message = is_bid_valid(form, id, request.user.id)
            if message is not False:
                messages.error(request, f"{message}")
                return HttpResponseRedirect(reverse("read", kwargs={
                    "id": id, 
                    "name": name,
                }))
            else:
                try:
                    new_bid = Bid.objects.create(
                        bid_price = form.cleaned_data["bid_price"],
                        bid_time = datetime.now(),
                        bidder = User.objects.get(pk=request.user.id),
                        listing = Listing.objects.get(pk=id),
                    )
                    new_bid.save()
                    messages.success(request, f"You've bid for {new_bid.listing.name}!")
                    return HttpResponseRedirect(reverse("read", kwargs={
                        "id": id, 
                        "name": name,
                    }))
                except IntegrityError as e:
                        messages.error(request, f"{e.__cause__}")
                        return HttpResponseRedirect(reverse("read", kwargs={
                        "id": id, 
                        "name": name,
                    }))
        else:
            messages.error(request, "Your bid failed to post: Form not valid.")
            return HttpResponseRedirect(reverse("read", kwargs={
                "id": id, 
                "name": name,
            }))
    else:
        messages.error(request, "Your bid failed to post: Method not POST.")
        return HttpResponseRedirect(reverse("read", kwargs={
            "id": id, 
            "name": name,
        }))


@login_required
def create_comment(request, id, name):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            try:
                new_comment = Comment.objects.create(
                    comment = form.cleaned_data["comment"],
                    commented = datetime.now(),
                    commenter = User.objects.get(pk=request.user.id),
                    listing = Listing.objects.get(pk=id),
                )
                new_comment.save()
                messages.success(request, f"Your comment is posted!")
                return HttpResponseRedirect(reverse("read", kwargs={
                    "id": id, 
                    "name": name,
                }))
            except IntegrityError as e:
                messages.error(request, f"{e.__cause__}")
                return HttpResponseRedirect(reverse("read", kwargs={
                "id": id, 
                "name": name,
            }))
        else:
            messages.error(request, "Your comment failed to post")
            return HttpResponseRedirect(reverse("read", kwargs={
                "id": id, 
                "name": name,
            }))

    else:
        messages.error(request, "Your comment failed to post")
        return HttpResponseRedirect(reverse("read", kwargs={
            "id": id, 
            "name": name,
        }))


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

    is_owner = False
    is_winner = False
    is_watched = False
    if request.user.is_authenticated:
        user = request.user
        if listing.lister == user:
            is_owner = True
        if listing.winner == user:
            is_winner = True
        if Watchlist.objects.filter(user=user, listing=listing).exists():
            is_watched = True

    if listing.is_active == False and is_owner == False and is_winner == False:
        messages.error(request, "Sorry, this listing was closed.")
        return HttpResponseRedirect(reverse("index"))

    bids = Bid.objects.filter(listing=id).order_by("-bid_time")
    comments = Comment.objects.filter(listing=id).order_by("-commented")

    return render(request, "auctions/read_listing.html", {
        "owner": is_owner,
        "watched": is_watched,
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "bidform": BidForm(),
        "commentform": CommentForm(),
    })


@login_required
def close_listing(request, id, name):
    listing = Listing.objects.get(id=id)
    max_bid = Bid.objects.filter(listing=id).aggregate(Max("bid_price"))['bid_price__max']
    winner = Bid.objects.get(listing=id, bid_price=max_bid).bidder
    # if winner == User.objects.get(id=request.user.id):
    #     pass
    try:
        listing.is_active = False
        listing.winner = winner
        listing.save()
        messages.success(request, 
            f"Your listing of {listing.name} is closed. \
            {winner.username} won your listing!")        
    except IntegrityError as e:
        messages.error(request, f"{e.__cause__}")

    return HttpResponseRedirect(reverse("index"))


@login_required
def read_my_bids(request):
    user = User.objects.get(id=request.user.id)
    bids = Bid.objects.filter(bidder=user).exclude(listing__lister=user)
    return render(request, "auctions/bids.html",{
        "header": f"{user.username}'s bids",
        "bids": bids
    })


@login_required
def read_my_comments(request):
    user = User.objects.get(id=request.user.id)
    comments = Comment.objects.filter(commenter=user)
    return render(request, "auctions/comments.html",{
        "header": f"{user.username}'s comments",
        "comments": comments
    })


@login_required
def read_my_listings(request):
    user = User.objects.get(id=request.user.id)    
    listings = Listing.objects.filter(lister=user).order_by("-id")
    return render(request, "auctions/index.html", {
        "header": f"{user.username}'s listings",
        "listings": listings
    })


@login_required
def read_my_watchlist(request):
    user = User.objects.get(id=request.user.id)
    watchlist = Watchlist.objects.filter(user=user)
    listings = Listing.objects.filter(
        watchlist__in=watchlist, is_active=True).order_by("-id")

    return render(request, "auctions/index.html", {
        "header": f"{user.username}'s watchlist",
        "listings": listings
    })


@login_required
def read_my_winnings(request):
    user = User.objects.get(id=request.user.id)
    listings = Listing.objects.filter(winner=user).order_by("-id")
    return render(request, "auctions/index.html", {
        "header": f"{user.username}'s winnings",
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
