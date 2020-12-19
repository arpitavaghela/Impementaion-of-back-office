from django.contrib import admin

#from .models import *
from . models import Customer, Order, Product

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)


admin.site.site_header = "Supply Chain Portal"
admin.site.site_title = "Supply Chain Portal"
admin.site.index_title = "Welcome to Supply Chain Portal"