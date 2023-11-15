from rest_framework import serializers
from .models import UserLikedBooks, UserCart, CartItem, UserPurchasesList, \
    PurchaseItem
from book.models import Book


class UserLikedBooksSerializer(serializers.Serializer):
    """
    Returns list of user's liked books.
    Always get only one instance, many=True for this serializers is
    restricted.
    Also need to pass book_slug:slug and added_to_liked:boolean as context.
    """
    id = serializers.IntegerField(read_only=True)
    user_liked_books = serializers.SerializerMethodField(
        method_name='get_liked_books', required=False)

    def get_liked_books(self, instance: UserLikedBooks):
        get_liked_books_query = instance.user_liked_books.all()
        return [{
            'id': book.id,
            'title': book.title,
            'slug': book.slug,
            'authors': [{
                'id': author.id,
                'name': author.name,
            } for author in book.authors.all()],
            'hardcoverPrice': book.hardcover_price,
            'paperbackPrice': book.paperback_price,
            'coverImage': book.cover_image.url
        } for book in get_liked_books_query]

    def update(self, instance: UserLikedBooks, validated_data):
        book_slug = self.context.get('book_slug')
        liked_exists = instance.user_liked_books.filter(
            slug=book_slug).exists()
        book = Book.objects.get(slug=book_slug)
        if liked_exists is True:
            instance.user_liked_books.remove(book)
        if liked_exists is False:
            instance.user_liked_books.add(book)
        return instance


class UserCartSerializer(serializers.Serializer):
    """
    Returns list of user's cart items(book data, quantity of required books
    and type of cover.
    Always get only one instance, many=True for this serializers is
    restricted.
    Also need to pass as serializer context:
    Operation type:str.
    If operation type is 'add':
        need to provide as context:
        - book_slug:slug
        - cover_type:string (hardcover/paperback)
        - quantity:int (number of books that will be bought, default is 1.
    If operation type is 'delete':
        need to provide as context:
        - cart_item_id:number (id of cart item that will be deleted).
    """
    id = serializers.IntegerField(read_only=True)
    userCart = serializers.SerializerMethodField(method_name='get_cart')

    def get_cart(self, instance: UserCart):
        cart_items_query = instance.cart_item.all()
        user_cart = [{
            'id': cart_item.id,
            'quantity': cart_item.quantity,
            'title': cart_item.book.title,
            'coverType': cart_item.cover_type,
            'coverImage': cart_item.book.cover_image.url,
            'price': cart_item.price,
            'authors': [{
                'id': author.id,
                'name': author.name,
            } for author in cart_item.book.authors.all()],
        } for cart_item in cart_items_query]
        return user_cart

    def update(self, instance: UserCart, validated_data):
        operation_type = self.context.get('operation_type')
        cover_type = self.context.get(
            'operation_type') if self.context.get(
            'operation_type') is not None else 'hardcover'
        if operation_type == 'add':
            book_slug = self.context.get('book_slug')
            book = Book.objects.get(slug=book_slug)
            cart_item = CartItem.objects.create(user_cart=instance,
                                                book=book,
                                                cover_type=cover_type,
                                                quantity=1,
                                                )
            cart_item.save()
            return instance
        if operation_type == 'remove':
            cart_item_id = self.context.get('cart_item_id')
            CartItem.objects.get(pk=cart_item_id).delete()
            return instance


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    book = serializers.SerializerMethodField(method_name='get_book',
                                             required=False)
    coverType = serializers.CharField(max_length=9, required=False,
                                      source='cover_type')
    quantity = serializers.IntegerField(allow_null=True, required=False)
    price = serializers.IntegerField()

    def get_related_user_email(self, instance: CartItem):
        return instance.user_cart.user_id.email

    def update(self, instance: CartItem, validated_data):
        if self.context.get('operation_type') == 'increase':
            book_quantity = instance.book.hardcover_quantity \
                if instance.cover_type == 'hardcover' \
                else instance.book.paperback_quantity

            probably_quantity = instance.quantity + 1
            if probably_quantity <= book_quantity:
                instance.quantity = probably_quantity
                instance.save()

        if self.context.get('operation_type') == 'decrease':
            probably_quantity = instance.quantity - 1
            if probably_quantity > 0:
                instance.quantity = probably_quantity
                instance.save()
        return instance

    def get_book(self, instance: CartItem):
        book = {'bookId': instance.book.id,
                'bookTitle': instance.book.title,
                'bookSlug': instance.book.slug}
        return book


class UserPurchasesListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    purchases = serializers.SerializerMethodField(method_name='get_purchases')

    def get_purchases(self, instance: UserPurchasesList):
        user_purchases_query = instance.purchase_items.all()

        purchase_items = [{
            'id': purchase_item.id,
            'quantity': purchase_item.quantity,
            'title': purchase_item.book.title,
            'coverImage': purchase_item.book.cover_image.url,
            'coverType': purchase_item.cover_type,
            'price': purchase_item.price,
            'authors': [{
                'name': author.name,
            } for author in purchase_item.book.authors.all()],
            'boughtTime': purchase_item.bought_time,
        } for purchase_item in user_purchases_query]

        return purchase_items

    def update(self, instance: UserPurchasesList, validated_data):
        cart_items_ids = self.context.get('cart_items_ids')
        cart_items_query = CartItem.objects.filter(pk__in=[*cart_items_ids])
        for cart_item in cart_items_query:
            purchase_item = PurchaseItem.objects.create(
                user_purchases_list=instance, book=cart_item.book,
                quantity=cart_item.quantity,
                cover_type=cart_item.cover_type
            )
            instance.purchase_items.add(purchase_item)
        cart_items_query.delete()
        return instance
