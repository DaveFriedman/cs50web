from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Listing, Bid, Comment


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        # Are fields lists[] or tuples()? it's confusing:
        # https://docs.djangoproject.com/en/4.0/topics/forms/modelforms/
        
        fields = ["name", "quantity", "category", "is_returnable", "list_price", 
                 "ship_price", "buynow_price", "description", "listing_timeout"]
        
        labels = {
            "name":             _("Item name"),
            "quantity":         _("Item quantity"),
            "category":         _("Item category"),
            "list_price":       _("Minimum bid"),
            "ship_price":       _("Shipping cost"),
            "buynow_price":     _("Buy now bid"),
            "description":      _("Item description"),
            "listing_timeout":  _("Auction length"),
            }

        help_texts = {
            "is_returnable":    _("Check if item is returnable"),
            "listing_timeout":  _("(in days)"),
        }

        # error_messages = {
        #     "quantity":         _("Quantity must be greater than zero"),
        #     "list_price":       _("Price must be greater than zero"),
        #     "buynow_price":     _("Price must be greater than zero"),
        #     "listing_timeout":  _("Auction must be at least 1 day"),
        # }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]



# class entry_form(forms.Form):

#     title = forms.CharField(
#         initial="title",
#         label="Title",
#         widget=forms.TextInput()
#         )
#     body = forms.CharField(
#         label="Body", 
#         widget=forms.Textarea()
#         )