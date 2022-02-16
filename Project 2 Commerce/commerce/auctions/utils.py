from django.db.models import Max
from .models import Bid, Listing

def is_bid_valid(bid_form, listing_id, user):
    message = False
    bid = bid_form.cleaned_data["bid_price"]
    bidder = user
    max_bid = Bid.objects.filter(listing=listing_id).aggregate(Max("bid_price"))['bid_price__max']
    max_bidder = Bid.objects.get(listing=listing_id, bid_price=max_bid).bidder
    lister = Listing.objects.get(id=listing_id).lister

    if bid <= max_bid:
        message = f"Current max bid is ${max_bid:.2f}. Your ${bid} bid must be higher."
    elif bidder == max_bidder:
        message = "You cannot raise your own max bid."
    elif bidder == lister:
        message = "You cannot bid on your own listing."
    return message