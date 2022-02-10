from django.db.models import Max
from .models import Bid, User

def is_bid_valid(bid_form, listing_id, user_id):
    message = False
    bid = bid_form.cleaned_data["bid_price"]
    max_bid = Bid.objects.filter(listing=listing_id).aggregate(Max("bid_price"))['bid_price__max']
    max_bidder = Bid.objects.get(listing=listing_id, bid_price=max_bid).bidder

    if bid <= max_bid:
        message = f"Current max bid is ${max_bid:.2f}. Your ${bid} bid must be higher."
    elif max_bidder == User.objects.get(id=user_id):
        message = "You cannot raise your own max bid."
    return message