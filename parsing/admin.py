from django.contrib import admin
from .models import SomonTjPhone,SomonTjCar,SomonTjCategoryParent,SomonTjPhoneCategory

# Register your models here.
admin.site.register(SomonTjCategoryParent)
admin.site.register(SomonTjPhoneCategory)
admin.site.register(SomonTjPhone)
admin.site.register(SomonTjCar)