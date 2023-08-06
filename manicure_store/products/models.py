from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    stripe_product_price_id = models.CharField(max_length=128, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} | {self.category.name}'


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    # user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    session = models.CharField(max_length=256, default=0)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def sum(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return self.session


class User(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    number = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name} | {self.number}'


class Ordered(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=Category, on_delete=models.PROTECT)



