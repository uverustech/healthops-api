from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Account(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )
    
    email_verified = models.BooleanField(default=False)
