from django.contrib import admin
from .models import Shoe, Basket, Favorite

# Register your models here.
admin.site.register(Shoe)
admin.site.register(Basket)
admin.site.register(Favorite)