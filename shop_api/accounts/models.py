from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Phone number"
    )

    def clean(self):
        if self.is_superuser and not self.phone_number:
            raise ValidationError({
                'phone_number': 'Phone number is required for superusers'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

