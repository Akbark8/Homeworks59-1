from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.title


from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    text = models.TextField()
    stars = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], default=0
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return f"{self.stars}⭐ - {self.product.title}"

    class UserConfirm(models.Model):
        user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name='confirm'
        )
        code = models.CharField(max_length=6)

        def __str__(self):
            return f"{self.user.username} - {self.code}"



