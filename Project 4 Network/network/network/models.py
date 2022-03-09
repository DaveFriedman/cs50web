from django.contrib.auth.models import AbstractUser
from django.db.models import *
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = EmailField(
        _('email address'),
        unique=True,
        error_messages={"unique": _("Not a valid email address.")}
        )
    timezone = DateTimeField()
    profile_pic = ImageField(upload_to="profile_pics")


class Post(Model):
    body = CharField(max_length=480)
    pic = ImageField(upload_to="post_pics")
    timestamp = DateTimeField(auto_now_add=True)

    author = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"PK: {self.id}, {self.user} wrote a post at {self.timestamp}"


class Like(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    post = ForeignKey(Post, on_delete=CASCADE)

    def __str__(self):
        return f"PK: {self.id}, User {self.user} liked {self.post}"


class Follow(Model):
    follower = ForeignKey(User, on_delete=CASCADE)
    creator = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return f"PK: {self.id}: {self.follower} follows {self.creator}"
