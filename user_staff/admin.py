from django.contrib import admin
from .models import UserFavouriteBooks, UserCart, CartItem, UserPurchasesList, \
    PurchaseItem

admin.site.register(UserFavouriteBooks)
admin.site.register(UserCart)
admin.site.register(CartItem)
admin.site.register(UserPurchasesList)
admin.site.register(PurchaseItem)
