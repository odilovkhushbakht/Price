from django.shortcuts import render
from django.views.generic import ListView
from django.db import transaction
from getproduct.settings import MEDIA_ROOT
import hashlib
from .models import SomonTjPhone
from .receive.somontj import SomonTj
import requests



class ListPhone(ListView):

    model = SomonTjPhone
    template_name = 'parsing/listphone.html'

    def get(self, request, *args, **kwargs):
        somontj = SomonTj()
        list_models = somontj.get_category('https://somon.tj/telefonyi-i-svyaz/mobilnyie-telefonyi/')
        list_phone = somontj.get_phone(list_models)
        return render(request,self.template_name)
