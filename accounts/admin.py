from django.contrib import admin

# Register your models here.
from .models import Order, TagOrder, Customer, Equipment, TagEquipment

admin.site.register(Order)
admin.site.register(TagOrder)
admin.site.register(Customer)
admin.site.register(Equipment)
admin.site.register(TagEquipment)
