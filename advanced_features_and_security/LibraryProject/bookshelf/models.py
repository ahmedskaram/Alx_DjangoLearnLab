from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_view", "Can view articles"),
            ("can_edit", "Can edit articles"),
            ("can_create", "Can create articles"),
            ("can_delete", "Can delete articles"),
        ]
    
    def __str__(self):
        return self.title

# -------------------------------------------------------------------------------------------

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

# -------------------------------------------------------------------------------------------

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth=None, profile_photo=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth, profile_photo=profile_photo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password=password, **extra_fields)

# -------------------------------------------------------------------------------------------

from django.contrib.auth.models import Group, Permission
# Create groups
editors_group, created = Group.objects.get_or_create(name='Editors')
viewers_group, created = Group.objects.get_or_create(name='Viewers')
admins_group, created = Group.objects.get_or_create(name='Admins')


# Assign permissions to groups
can_edit_permission = Permission.objects.get(codename='can_edit')
can_create_permission = Permission.objects.get(codename='can_create')
can_view_permission = Permission.objects.get(codename='can_view')
can_delete_permission = Permission.objects.get(codename='can_delete')

editors_group.permissions.add(can_edit_permission, can_create_permission)
viewers_group.permissions.add(can_view_permission)
admins_group.permissions.add(can_edit_permission, can_create_permission, can_view_permission, can_delete_permission)

# -------------------------------------------------------------------------------------------
