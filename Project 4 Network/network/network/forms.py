from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, EmailInput, ModelForm, Textarea

from .models import User, Post


class SignUpForm(UserCreationForm):
    email = CharField(max_length=254, required=False, widget=EmailInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "bio",
            "profile_pic_url",
            ]
        widgets = {"bio": Textarea(attrs={
            "rows": 6
            })}


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["body"]
        labels = {"body": False}
        widgets = {"body": Textarea(attrs={
            "rows": 6,
            "placeholder": "What's on your mind?",
        })}
