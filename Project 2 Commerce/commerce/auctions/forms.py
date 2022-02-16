from django.forms import ModelForm, NumberInput, Textarea, ValidationError

from .models import Listing, Bid, Comment


class ListingForm(ModelForm):
    def clean_list_price(self):
        list_price = self.cleaned_data["list_price"]
        if list_price <= 0:
            raise ValidationError("Minimum bid must be greater than 0")
        return list_price

    class Meta:
        model = Listing

        fields = ["name", "category", "description", "image_url", "list_price"]

        labels = {
            "name": "Item name",
            "category": "Item category",
            "description": "Item description",
            "image_url": "Link to an image of the item (optional)",
            "list_price": "Opening bid",
        }

        widgets = {"description": Textarea(attrs={
            "rows": 6,
            })}


class BidForm(ModelForm):
    def clean_bid_price(self):
        bid = self.cleaned_data["bid_price"]
        if bid <= 0:
            raise ValidationError("Bid must be greater than 0")
        return bid

    class Meta:
        model = Bid
        fields = ["bid_price"]
        labels = {"bid_price": False}
        widgets = {"bid_price": NumberInput(attrs={
            "placeholder": "Add a bid"
            })}
         

class CommentForm(ModelForm):
    def clean_comment(self):
        comment = self.cleaned_data["comment"]
        if comment == None or comment == "":
            raise ValidationError("Comment cannot be empty")
        return comment

    class Meta:
        model = Comment
        fields = ["comment"]
        labels = {"comment": False}
        widgets = {"comment": Textarea(attrs={
            "placeholder": "Add a comment",
            "rows": 2,
            })}
