from django.forms import ModelForm, Textarea

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        labels = {"body" : "What's on your mind?"}
        widgets = {"body" : Textarea(attrs={"rows": 4})}