from django.contrib import admin
from .models import UserLikedBooks, UserCart, CartItem, UserPurchasesList, \
    PurchaseItem

admin.site.register(UserLikedBooks)
admin.site.register(UserCart)
admin.site.register(CartItem)
admin.site.register(UserPurchasesList)
admin.site.register(PurchaseItem)
