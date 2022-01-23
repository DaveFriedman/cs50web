from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):

    name = models.CharField(max_length=64)
    quantity = models.IntegerField(default=1)
    is_returnable = models.BooleanField()
    description = models.TextField(max_length=480)

    list_price = models.DecimalField(decimal_places=2)
    buynow_price = models.DecimalField(decimal_places=2)    
    ship_price = models.DecimalField(decimal_places=2)

    listing_start = models.DateTimeField(auto_now_add=True)
    listing_end = models.DateTimeField()
    listing_timeout = models.DateTimeField()

    lister = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Listing {self.id}: {self.lister}'s {self.name}"

    def verbose(self):
        return f"Listing {self.id}: {self.lister}'s ({self.quantity}) \
                {self.name}, returnable={self.is_returnable} {chr(10)} \
                listed on {self.listing_start} for ${self.list_price} + \
                ${self.ship_price}, {chr(10)} \
                times out {self.listing_timeout}, buynow ${self.buynow_price} \
                hit at {self.listing_end} {chr(10)} \
                description: {self.description}"


class Bid():

    bid_price = models.DecimalField(decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)

    def __str__(self):
        return f"Bid {self.id}: {self.bid_price} on {self.listing}"
        
    def verbose(self):
        return f"Bid {self.id}: {self.bidder} bid {self.bid_price} on  \
                {self.listing} at {self.bid_time}"


class Comment():

    comment = models.TextField(max_length=280)
    is_hidden = models.BooleanField()

    commented = models.DateTimeField(auto_now_add=True)
    commenter = models.ForeignKey('User')

    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    parent = models.ForeignKey('self')

    def __str__(self):
        return f"Comment {self.id}: {self.commenter} posted on {self.listing}"

    def verbose(self):
        return f"Comment {self.id}: At {self.commented}, on {self.listing}, \
                {self.commenter} replied to {self.parent}, saying: {chr(10)} \
                {self.comment} {chr(10)} (hidden={self.is_hidden})"
