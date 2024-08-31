from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Shoe(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('kid', 'Kid'),
    ]
    
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    stars = models.DecimalField(max_digits=3, decimal_places=1)  # Example: 4.5
    available_sizes = models.JSONField()  # Store an array of sizes, e.g. [38, 39, 40, 41]
    color = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='shoes/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'shoe')

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shoe = models.ForeignKey(Shoe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'shoe')
