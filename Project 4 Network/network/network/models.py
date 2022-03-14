from django.contrib.auth.models import AbstractUser
from django.db.models import *


class User(AbstractUser):
    pass


class Post(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    body = TextField(max_length=280)
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id}: by {self.author} at {self.timestamp}"


class Like(Model):
    post = ForeignKey(Post, on_delete=CASCADE)
    liker = ForeignKey(User, on_delete=CASCADE)
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: at {self.timestamp}, {self.liker} liked {self.post}"


class Follow(Model):
    creator = ForeignKey(User, on_delete=CASCADE, related_name="creator")
    follower = ForeignKey(User, on_delete=CASCADE, related_name="follower")
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.follower} follows {self.creator}"