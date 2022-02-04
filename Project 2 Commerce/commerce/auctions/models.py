from django.contrib.auth.models import AbstractUser
from django.db.models import *
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Listing(Model):

    class categories(TextChoices):
        """
        Ebay categories: Electronics, Collectibles & Art, Fashion, Motors, Toys  
        & Hobbies, Sports, Health & Beauty, Books, Movies & Music, Business & 
        Industrial, Home & Garden, Others
        """
        ELECTRONICS =         "EL", _("Electronics")
        COLLECTIBLES_ART =    "CO", _("Collectibles & Art")
        FASHION =             "FA", _("Fashion")
        MOTORS =              "MO", _("Motors")
        TOYS_HOBBIES =        "TO", _("Toys & Hobbies")
        SPORTS =              "SP", _("Sports")
        HEALTH_BEAUTY =       "HE", _("Health & Beauty")
        BOOKS_MOVIES_MUSIC =  "BO", _("Books, Movies & Music")
        BUSINESS_INDUSTRIAL = "BU", _("Business & Industrial")
        HOME_GARDEN =         "HO", _("Home & Garden")
        OTHER =               "OT", _("Other")

    name = CharField(max_length=64)
    category = CharField(choices=categories.choices, max_length=24)
    description = TextField(max_length=480)
    image_url = URLField(blank=True)
    list_price = DecimalField(max_digits=9, decimal_places=2)
    
    is_active = BooleanField()

    lister = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"Listing {self.id}: {self.lister}'s {self.name}"

    # def verbose(self):
    #     return f"Listing {self.id}: {self.lister}'s ({self.quantity}) \
    #             {self.name}, {self.is_returnable=}, {self.category=} {chr(10)} \
    #             listed on {self.listing_start} for ${self.list_price} + \
    #             ${self.ship_price}, {chr(10)} \
    #             times out {self.listing_timeout}, buynow ${self.buynow_price} \
    #             hit at {self.listing_end} {chr(10)} \
    #             description: {self.description}"


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
        return f"PK: {self.id}, User {self.user} watches listing {self.listing}"