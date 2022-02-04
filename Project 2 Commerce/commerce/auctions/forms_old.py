from django.forms import DateTimeInput, ModelForm, ValidationError 
from django.utils.translation import gettext_lazy as _

from .models import Listing, Bid, Comment


class ListingForm(ModelForm):

    # def clean_quantity(self):
    #     quantity = self.cleaned_data["quantity"]
    #     if quantity <= 0:
    #         raise ValidationError("Quantity must be greater than 0")
    #     return quantity


    def clean_list_price(self):
        list_price = self.cleaned_data["list_price"]
        if list_price <= 0:
            raise ValidationError("Minimum bid must be greater than 0")
        return list_price


    # def clean_ship_price(self):
    #     ship_price = self.cleaned_data["ship_price"]
    #     if ship_price < 0:
    #         raise ValidationError("Shipping cost must be 0 or greater")
    #     return ship_price


    # def clean_buynow_price(self):
    #     buynow_price = self.cleaned_data["buynow_price"]
    #     if buynow_price <= 0:
    #         raise ValidationError("Buy now bid must be greater than 0")
    #     return buynow_price


    class Meta:
        model = Listing
        
        # fields = ["name", "quantity", "category", "is_returnable", "list_price", 
        #          "ship_price", "buynow_price", "description", "listing_timeout"]

        fields = ["name", "category", "description", "image_url", "list_price"]

        # widgets = {'listing_timeout': DateTimeInput}
        
        labels = {
            "name":             _("Item name"),
            # "quantity":         _("Item quantity"),
            "category":         _("Item category"),
            # "is_returnable":    _("Check if item is returnable"),
            "description":      _("Item description"),
            "image_url":       _("Link to an image of the item (optional)")

            # "list_price":       _("Minimum bid"),
            # "ship_price":       _("Shipping cost"),
            # "buynow_price":     _("Buy now bid"),

            # "listing_timeout":  _("End of auction"),
            }

        help_texts = {
            # "listing_timeout":  _("(in days)"),
        }

        error_messages = {
        #     "quantity":         _("Quantity must be greater than zero"),
        }


class BidForm(ModelForm):

    def clean_bid(self):
        bid = self.cleaned_data["bid"]
        if bid <= 0:
            raise ValidationError("Bid must be greater than 0")        
        return bid

    class Meta:
        model = Bid
        fields = ["bid_price"]


class CategoryForm(ModelForm):
    class Meta: 
        model = Listing
        fields = ["category"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
