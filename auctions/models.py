from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    starting_bid = models.FloatField()
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categ",  blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    date = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    comment = models.CharField(max_length=100)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.listing}: {self.comment}"


class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.listing}: {self.bid}"
