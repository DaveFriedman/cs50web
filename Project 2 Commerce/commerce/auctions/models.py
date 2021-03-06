from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    pass


class Listing(Model):
    # Categories via ebay
    CATEGORIES = (
        ("BO", "Books, Movies & Music"),
        # ("BU", "Business & Industrial"),
        ("CO", "Collectibles & Art"),
        # ("EL", "Electronics"),
        ("FA", "Fashion"),
        # ("HE", "Health & Beauty"),
        # ("HO", "Home & Garden"),
        # ("MO", "Motors"),
        # ("SP", "Sports"),
        # ("TO", "Toys & Hobbies"),
        ("OT", "Other"),
    )

    name = CharField(max_length=64)
    category = CharField(choices=CATEGORIES, max_length=2)
    description = TextField(max_length=480)
    image_url = URLField(blank=True)
    list_price = DecimalField(max_digits=9, decimal_places=2)
    is_active = BooleanField()

    lister = ForeignKey(User, on_delete=CASCADE, related_name="lister")
    winner = ForeignKey(User, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return f"Listing {self.id}: {self.lister}'s {self.name}"

    def verbose(self):
        return f"Listing {self.id}: {self.lister}'s {self.name}, \
                 for ${self.list_price}, {self.is_active=}, {self.category=}, \
                 {chr(10)} {self.image_url=}, {chr(10)} {self.description=}. \
                 {chr(10)} Won by {self.winner}."

    def category_displayname(code):
        """
        Couldn't figure out the django way to get the display name of just 1
        category, so here we are.        
        """
        displayname = dict(Listing._meta.get_field("category").choices)[code]
        return displayname


class Bid(Model):
    bid_price = DecimalField(max_digits=9, decimal_places=2)
    bid_time = DateTimeField(auto_now_add=True)

    bidder = ForeignKey(User, on_delete=CASCADE)
    listing = ForeignKey(Listing, on_delete=CASCADE, related_name="auction")

    def __str__(self):
        return f"Bid {self.id}: {self.bidder} bid {self.bid_price} on  \
                {self.listing} at {self.bid_time}"


class Comment(Model):
    comment = TextField(max_length=280)
    commented = DateTimeField(auto_now_add=True)

    commenter = ForeignKey(User, on_delete=CASCADE)
    listing = ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f"Comment {self.id}: {self.commenter} posted on {self.listing}"

    def verbose(self):
        return f"Comment {self.id}: At {self.commented}, on {self.listing}, \
                {self.commenter} wrote: {chr(10)} {self.comment}"


class Watchlist(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    listing = ForeignKey(Listing, on_delete=CASCADE)

    def __str__(self):
        return f"PK: {self.id}, User {self.user} watches {self.listing}"
