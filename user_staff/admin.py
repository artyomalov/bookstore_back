from django.contrib import admin
from .models import UserLikedBooks, UserCart, CartItem, UserPurchasesList, \
    PurchaseItem


@admin.register(UserLikedBooks)
class UserLIkedBooksAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_user_liked_books_quantity')
    list_display_links = ('id', 'get_user_email',)
    ordering = ('id',)

    @admin.display(description='user email')
    def get_user_email(self, model: UserLikedBooks):
        return model.user_id.email

    @admin.display(description='user liked books\' quantity')
    def get_user_liked_books_quantity(self, model: UserLikedBooks):
        return model.user_liked_books.count()


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_user_cart_size')
    list_display_links = ('id', 'get_user_email')
    ordering = ('id',)

    @admin.display(description='user email')
    def get_user_email(self, model: UserCart):
        return model.user_id.email

    @admin.display(description='in cart books\' quantity')
    def get_user_cart_size(self, model: UserCart):
        return model.cart_item.count()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_cart', 'book', 'quantity', 'cover_type')
    list_display_links = ('id', 'user_cart')
    list_editable = ('cover_type',)
    ordering = ('id',)


@admin.register(UserPurchasesList)
class UserPurchasesListAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_email', 'get_user_purchase_items_size')
    list_display_links = ('id', 'get_user_email')
    ordering = ('id',)

    @admin.display(description='user email')
    def get_user_email(self, model: UserPurchasesList):
        return model.user_id.email

    @admin.display(description='bought books\' quantity')
    def get_user_purchase_items_size(self, model: UserPurchasesList):
        return model.purchase_items.count()


@admin.register(PurchaseItem)
class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_purchases_list', 'book', 'quantity', 'cover_type',
        'bought_time',)
    list_display_links = ('id', 'user_purchases_list',)
    list_editable = ('cover_type',)
    ordering = ('id',)
