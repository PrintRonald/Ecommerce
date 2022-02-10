from django.db import models
# importamos el modelo de usuario por defecto de django
from django.contrib.auth.models import User

# creamos el modelo de cliente


class Customer(models.Model):
    # relacion uno a uno con modelo usuario
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# modelo de producto


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

# modelo de pedido


class Order(models.Model):
    # relacion uno es a mucho entre pedido y cliente
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    # estado de completo (por defecto es falso)
    complete = models.BooleanField(default=False)
    # identificacion de la transaccion
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

# modelo de articulo de pedido


class OrderItem(models.Model):
    # atributo producto conectado al modelo de producto
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # atributo de pedido conectado al modelo de pedido
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    # cantidad
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # fecha en que se registra el producto
    date_added = models.DateTimeField(auto_now_add=True)

# modelo de envio


class ShippingAddress(models.Model):
    # conectamos con el modelo cliente para que un cliente pueda
    # reutilizar la direccion de envio en el futuro
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
