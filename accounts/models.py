from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profilepic.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class EquipmentTag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    CATEGORY = (
        ('Molde', 'Molde'),
        ('Maquina', 'Maquina'),
    )

    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    equipment_tags = models.ManyToManyField(EquipmentTag)

    def __str__(self):
        return self.name

class OrderTag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('En revisión', 'En revisión'),
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    equipo = models.ForeignKey(Equipment, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    descripción = models.CharField(max_length=1000, null=True)
    order_tags = models.ManyToManyField(OrderTag)
    #imagen = models.ImageField(default="profilepic.jpg", null=True, blank=True)
    #video = models.ImageField(default="profilepic.jpg", null=True, blank=True)

    def __str__(self):
        return self.equipo.name
