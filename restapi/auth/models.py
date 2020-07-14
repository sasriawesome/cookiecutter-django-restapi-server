import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        editable=False)
    
    first_name = None
    last_name = None
    full_name = models.CharField(_('full name'), max_length=30, blank=False)
    short_name = models.CharField(_('short name'), max_length=150, blank=True)

    def get_full_name(self):
        """
        Return the fullname.
        """
        return self.full_name

    def get_short_name(self):
        """Return the short name for the user."""
        return self.short_name