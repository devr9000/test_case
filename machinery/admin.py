from django.contrib import admin
from .models import BrandCatalog, TruckCatalog, Truck

admin.site.register(BrandCatalog)
admin.site.register(TruckCatalog)
admin.site.register(Truck)