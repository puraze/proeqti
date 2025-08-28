from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    LANGUAGE_CHOICES = [
        ("all", "All Languages"),
        ("en", "English"),
        ("ka", "Georgian"),
        ("ru", "Russian"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    views = models.PositiveIntegerField(default=0)
    language_visibility = models.CharField(
        max_length=10, choices=LANGUAGE_CHOICES, default="all"
    )

    def __str__(self):
        return self.name
