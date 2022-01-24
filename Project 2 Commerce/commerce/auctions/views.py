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
        "listings": models.Listing.objects.all()
    })

@login_required
def create_listing(request):

    if request.method == "POST":
        form = forms.ListingForm(request.POST)

        if form.is_valid():
            form.save()

            # name = form.cleaned_data['name']
            # quantity = form.cleaned_data['quantity']
            # is_returnable = form.cleaned_data['is_returnable']
            # category = form.cleaned_data['category']
            # description = form.cleaned_data['description']

            # list_price = form.cleaned_data['list_price']
            # ship_price = form.cleaned_data['ship_price']
            # buynow_price = form.cleaned_data['buynow_price']

            # listing_timeout = form.cleaned_data['listing_timeout']

        pass

    else:
        return render(request, "auctions/create_listing.html", {
            "form": forms.ListingForm()
        })


def read_listing(request, id, name):
    """
    TODO: Comments
    """
    listing = models.Listing.objects.get(id=id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required
def update_listing(request):
    pass


@login_required
def delete_listing(request):
    pass


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
