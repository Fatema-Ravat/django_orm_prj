""" Models for our inventory project """

from django.db import models
from django.contrib.auth.models import User

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

class Category(models.Model):
    """ Product Category model"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    is_active = models.BooleanField(default=True)
    level = models.SmallIntegerField(default=0)

    parent_id = models.ForeignKey("self",null=True,blank=True,on_delete=models.RESTRICT)

    class Meta:
        ordering = ["name"]
    
    objects=CategoryManager()

    def __str__(self):
        return f"{self.id}-{self.name}"
    
class Product(models.Model):
    """ Product  model"""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=55, unique=True)
    description = models.TextField(null=True,blank=True)
    is_digital = models.BooleanField(default =False)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,editable=False)

    category_id = models.ForeignKey(
                    Category,
                    on_delete=models.RESTRICT,
                    related_name="product_category"
                    )


    class Meta:
        ordering=["name"]

    def __str__(self):
        return self.name

# User Model
'''class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username
'''
    
class Order(models.Model):
    """ Order placed model"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    products = models.ManyToManyField(Product,through='OrderProduct')
    
    class Meta:
        ordering=["-created_date"]

    def __str__(self):
        return f"Order {self.id} created by {self.user.username}"
    
class OrderProduct(models.Model):
    """ Product in an order model"""

    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE )
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order","product"], name ="unique_product_per_order")
        ]

    def __str__(self):
        return f"{self.product}- Order {self.order.id}"
    
class StockManagement(models.Model):
    """ Product stock management model"""
    product = models.OneToOneField(  
                        Product,
                        on_delete=models.CASCADE,
                        unique=True,
                        related_name='stock')
    quantity = models.IntegerField()
    last_checked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock {self.product.name} - {self.quantity}"
    
class PriceReductionChoices(models.IntegerChoices):
    FIVE= 5,"5%"
    TEN = 10,"10%"
    TWENTY = 20,"20%"
    FIFTY = 50,"50%"

class PromotionEvent(models.Model):
    """ Promotion event model"""

    name = models.CharField(max_length=50,unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price_reduction = models.IntegerField(choices=PriceReductionChoices.choices)
    #products = models.ManyToManyField(Product) -- No need to explicitly create below table
                                            # -- Django does it for you.
    products = models.ManyToManyField(Product, through='ProductPromotionEvent')
    #through field used to tell django not to create new table and use this table.          
    class Meta:
        ordering =["-start_date"]

    def __str__(self):
        return self.name
    
class ProductPromotionEvent(models.Model):
    """ Product in promotion event model"""
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    promotion_event = models.ForeignKey(PromotionEvent,on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["product","promotion_event"], name="unique_product_for_promotion")
        ]
       
    def __str__(self):
        return f"{self.product.name}-{self.promotion_event.name}"