from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Customer(models.Model):
    AREA = (
        ('Mantenimiento', 'Mantenimiento'),
        ('Producción', 'Producción'),
        ('Administrativo', 'Administrativo')
    )
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="profilepic.jpg",
                                    null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    area = models.CharField(max_length=200, null=True, choices=AREA)

    def __str__(self):
        return self.name


class TagEquipment(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    CATEGORY = (
        ('Molde', 'Molde'),
        ('Maquina', 'Maquina'),
        ('Periferico', 'Periferico'),
    )

    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(TagEquipment, blank=True)

    def __str__(self):
        return self.name


class TagOrder(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('En revisión', 'En revisión'),
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada'),
    )
    customer = models.ForeignKey(Customer, null=True,
                                 on_delete=models.SET_NULL,
                                 related_name='customer')
    equipo = models.ForeignKey(
        Equipment, null=True, on_delete=models.SET_NULL, related_name='equipo')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_closed = models.DateTimeField(auto_now_add=False, null=True,
                                       blank=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    title = models.CharField(max_length=200, null=True)
    descripcion = models.CharField(max_length=1000, null=True)
    order_tags = models.ManyToManyField(TagOrder)
    # asigned_to = models.ForeignKey(
    #     Customer, null=True, on_delete=models.SET_NULL, blank=True,
    #     related_name='assigned_to')
    # imagen = models.ImageField(null=True, blank=True)
    # video = models.ImageField(default="profilepic.jpg", null=True, blank=True)

    def __str__(self):
        if self.date_created:
            date = self.date_created.strftime("%Y/%m/%d")
        else:
            date = "Any"
        return f"{str(self.equipo)}-{date}"


class OrderComments(models.Model):
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    author = models.ForeignKey(Customer, null=True,
                               on_delete=models.SET_NULL)
    descripcion = models.CharField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        date = self.date_created.strftime("%Y/%m/%d")
        return f"{str(self.order)}-{date}"


class Images(models.Model):
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return str(self.image)


class Videos(models.Model):
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    video = models.FileField(upload_to='videos/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return str(self.video)
