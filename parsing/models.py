from django.db import models
from getproduct.settings import MEDIA_ROOT


class SomonTjPhone(models.Model):

    name = models.CharField(max_length=255,verbose_name='name')
    price = models.FloatField(verbose_name='price')
    image = models.ImageField(upload_to=MEDIA_ROOT,verbose_name='image')
    current = models.CharField(max_length=3,verbose_name='current')
    url = models.URLField(verbose_name='url')

class SomonTjCar(models.Model):

    name = models.CharField(max_length=255,verbose_name='name')
    price = models.FloatField(verbose_name='price')
    image = models.ImageField(upload_to=MEDIA_ROOT,verbose_name='image')
    current = models.CharField(max_length=3,verbose_name='current')
    url = models.URLField(verbose_name='url')

class SomonTjPhoneCategory(models.Model):

    name = models.CharField(max_length=255,verbose_name='name')
    parent = models.ForeignKey('SomonTjCategoryParent',on_delete=models.CASCADE)


class SomonTjCategoryParent(models.Model):

    name = models.CharField(max_length=255, verbose_name='name')
    child = models.IntegerField(verbose_name='child')
