from django.contrib import admin
from .models import UserPurchasesList, PurchaseItem

# Register your models here.
admin.site.register(UserPurchasesList)
admin.site.register(PurchaseItem)
