from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    bio = TextField(max_length=280, blank=True)
    profile_pic_url = URLField(blank=True)


class Post(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    body = TextField(max_length=280)
    posted = DateTimeField(auto_now_add=True)
    edited = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id}: by {self.author} at {self.posted}"


class Like(Model):
    post = ForeignKey(Post, on_delete=CASCADE)
    liker = ForeignKey(User, on_delete=CASCADE)
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id}: {self.liker} liked {self.post} ({self.timestamp})"


class Follow(Model):
    creator = ForeignKey(User, on_delete=CASCADE, related_name="creator")
    follower = ForeignKey(User, on_delete=CASCADE, related_name="follower")
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id}: {self.follower} follows {self.creator}"
