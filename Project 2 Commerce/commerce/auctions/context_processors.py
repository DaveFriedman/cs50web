from .models import Listing

CATEGORIES = Listing._meta.get_field('category').choices

# https://stackoverflow.com/questions/34902707/how-can-i-pass-data-to-django-layouts-like-base-html-without-having-to-provi
def add_categories_to_context(request):
    return {"categories": CATEGORIES}
