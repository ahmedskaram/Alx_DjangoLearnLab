from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # User's biography
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Profile picture upload
    following = models.ManyToManyField(
        'self',  # Self-referential relationship
        symmetrical=False,  # One-way relationship (user A can follow user B without B following A)
        related_name='followers',  # Reverse relationship for followers
        blank=True
    )

    def __str__(self):
        return self.username
