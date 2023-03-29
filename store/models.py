from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE , default='')
    price = models.IntegerField()
    image = models.ImageField(upload_to='productimage/images')
    
    def __str__(self):
        return self.name
 
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product
    
class OrderDetails(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=100)
    houseno = models.CharField(max_length=100)
    postalno = models.IntegerField(default='')
    zip = models.IntegerField()

    def __str__(self):
        return self.country
    


    
class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password= models.CharField(max_length=500)

    def __str__(self):
        return self.firstname
    
    @staticmethod
    def get_customer_by_email(email=email):
        try:
            return Customer.objects.get(email=email)
        except:
            return False
        
    
    


