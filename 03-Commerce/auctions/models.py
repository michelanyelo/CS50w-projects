from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # generate a slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name="bids")
    amount = models.FloatField()

    def __str__(self):
        return f"{self.bidder.username} bids ${self.amount} on {self.listing.title}"


class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=1000)
    bid = models.ForeignKey(
        Bid,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="listings"
    )
    is_active = models.BooleanField(default=False, blank=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="category"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.author} comment on {self.listing}"


class UserWatchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s watchlist entry for {self.listing.title}"
