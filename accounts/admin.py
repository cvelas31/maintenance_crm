from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Order)
admin.site.register(TagOrder)
admin.site.register(Customer)
admin.site.register(Equipment)
admin.site.register(TagEquipment)
