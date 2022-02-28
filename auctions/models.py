from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.category}"
    
    class Meta:
        # If this isn’t given, Django will use verbose_name + "s". So in this case it would show Categorys
        verbose_name_plural = "Categories"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField ()
    starting_price = models.FloatField()
    current_bid = models.FloatField(default=0)
    current_bid_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_winner", blank=True, null=True)
    image_url = models.URLField(default="https://programacion.net/files/article/20161110041116_image-not-found.png")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listing_category",  blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_author")
    date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    
    def descripton_firts_p(self):
        return self.description.split('\n')[0]


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.listing}: {self.content}"


class Bid(models.Model):
    price = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")

    def __str__(self):
        return f"{self.user}: {self.listing}: {self.price}"


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")

    def __str__(self):
        return f"{self.user}: {self.listing}"
