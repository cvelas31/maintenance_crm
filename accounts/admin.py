from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(EquipmentTag)
admin.site.register(Equipment)
admin.site.register(OrderTag)
admin.site.register(Order)