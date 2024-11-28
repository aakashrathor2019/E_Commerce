from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    username = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    contact = models.IntegerField(unique=True)
    address = models.TextField()
    password=models.CharField(max_length=50)
     

    def __str__(self):
        return self.username

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'

class OrderItem(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE ,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    status = models.CharField(max_length=20, default="Pending",null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class WishlistItem(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_wishlist_item')
        ]

    def __str__(self):
        return f'{self.product.name} in {self.user.username}\'s wishlist'

class CartItem(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_cart_item')
        ]

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.user.username}\'s cart'




#Changed Database
# from django.db import models
# from django.contrib.auth.models import User


# class AppUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     username = models.CharField(max_length=200)
#     email = models.EmailField(max_length=50, unique=True)
#     contact = models.IntegerField(unique=True)
#     address = models.TextField()
#     password = models.CharField(max_length=50)

#     def __str__(self):
#         return self.username


# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name


# class Product(models.Model):
#     name = models.CharField(max_length=300, unique=True)  # Ensures no duplicate product names
#     desc = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.PositiveIntegerField()  # Ensure no negative stock values
#     image = models.ImageField(upload_to='products/')
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

#     def __str__(self):
#         return self.name

#     def reduce_stock(self, quantity):
#         """Reduce stock by the ordered quantity."""
#         if self.stock >= quantity:
#             self.stock -= quantity
#             self.save()
#         else:
#             raise ValueError("Insufficient stock!")


# class Order(models.Model):
#     user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='orders')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     status = models.CharField(max_length=20, default="Pending")

#     def __str__(self):
#         return f'Order {self.id} by {self.user.username}'


# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')  # Relationship with Order
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f'{self.quantity} x {self.product.name} in Order {self.order.id}'


# class WishlistItem(models.Model):
#     user = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='wishlist_items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_items')

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user', 'product'], name='unique_wishlist_item')
#         ]

#     def __str__(self):
#         return f'{self.product.name} in {self.user.username}\'s wishlist'


# class CartItem(models.Model):
#     user = models.OneToOneField(AppUser, on_delete=models.CASCADE, related_name='cart')  # One-to-one relationship
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
#     quantity = models.PositiveIntegerField(default=1)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['user', 'product'], name='unique_cart_item')
#         ]

#     def __str__(self):
#         return f'{self.quantity} x {self.product.name} in {self.user.username}\'s cart'

