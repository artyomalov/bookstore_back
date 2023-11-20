"""
Get sum of user's cart items prices
"""

__all__ = ['get_total', ]

from user_staff.models import CartItem
from django.db.models import Sum
from django.db.models import F


def get_total():
    total_dict = CartItem.objects.filter(user_cart__id=1).annotate(
        total=F('price') * F('quantity')).aggregate(total=Sum('total'))
    return total_dict.get('total')

