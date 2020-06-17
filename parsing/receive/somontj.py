from bs4 import BeautifulSoup
import requests
import hashlib
import threading
from multiprocessing import Pool
from getproduct.settings import MEDIA_ROOT
from ..models import SomonTjPhone


class SomonTj(threading.Thread):

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.38 Safari/537.36'}
    #models = list()

    def __init_(self):
        self.__init_(self,models)
        self.models = list()

    # получает категории из сайта
    def get_category(self,url:str=None):
        conn = requests.get(url,headers=self.header)
        html_text = conn.text
        bs = BeautifulSoup(html_text, 'lxml')
        models = bs.find('ul', {'class':['js-toggle-content','toggle-content']},True)
        models = models.find_all('li')
        models_list = list()
        temporary_data = dict()
        size = len(models)
        for current in range(size):
            temporary_data['name'] = models[current].get_text()
            temporary_data['link'] = 'https://somon.tj' + models[current].a['href']
            temporary_data['quantity'] = models[current].p.get_text()
            models_list.append(temporary_data.copy())
        self.models = models_list
        return models_list

    # получает все товары на указанном ссылке
    # def get_phone(self,models:list=None):
    #     list_phones = list()
    #     size = len(models)
    #     for current_model in range(size):
    #         url = models[current_model]['link']
    #         quantity_page = self.get_quantity_page(url)
    #         for current_page in range(quantity_page):
    #             url + '?page=' + current_page.__str__()
    #             phone_on_page = self.phone(url)
    #             list_phones.append(phone_on_page)
    #             self.save_to_base(phone_on_page)
    #     return list_phones


    def get_phone(self,models:list=None):
        list_phones = list()
        #size = len(models)
        #for current_model in range(size):
        with Pool(20) as p:
            p.map(self.one,self.models)
        return list_phones

    def one(self,models):
        url = models[current_model]['link']
        quantity_page = self.get_quantity_page(url)
        for current_page in range(quantity_page):
            url + '?page=' + current_page.__str__()
            phone_on_page = self.phone(url)
            list_phones.append(phone_on_page)
            self.save_to_base(phone_on_page)

    # получает все товары и вернет в виде списка из указанной странице
    def phone(self,url:str=None):
        conn = requests.get(url,headers=self.header)
        html_text = conn.text
        bs = BeautifulSoup(html_text, 'lxml')
        phones = bs.find('ul',{'class': ['list-simple__output', 'js-list-simple__output']},True)
        phones = phones.find_all('li',class_ = 'announcement-container',recursive=True)
        phone = dict()
        phone_list = []
        size = len(phones)
        for current in range(size):
            info = phones[current].find('div', {'class': 'announcement-block__price'}, True)
            phone['name'] = info.find('meta',itemprop='name')['content']
            phone['price'] = info.find('meta', itemprop='price')['content']
            phone['current'] = info.find('meta',itemprop='priceCurrency')['content']
            image = phones[current].find('img', {'itemprop': 'image'})
            phone['id'] = phones[current].find('div',
                            class_= {
                                'announcement-block__favorites','js-add-favorites','js-favorites-handler'
                            })['data-id']
            phone['image'] = None if image == None else image['src']
            phone['url'] = phones[current].find('a')['href']
            phone_list.append(phone.copy())
        return phone_list

    # Вернет количество пагинации
    def get_quantity_page(self,url:str=None):
        print(url)
        conn = requests.get(url,headers=self.header)
        html_text = conn.text
        bs = BeautifulSoup(html_text, 'lxml')
        page_quantity = bs.find('ul', class_ = 'number-list')
        if page_quantity == None:
            return 1
        else:
            return int(page_quantity.find_all('a')[-1]['data-page'])


    def save_to_base(self,data:list=None):
        if not data:
            return
        size = len(data)
        for item in range(size):
            somontjphone = SomonTjPhone()
            somontjphone.name = data[item]['name']
            somontjphone.price = data[item]['price']
            somontjphone.current = data[item]['current']
            somontjphone.url = data[item]['url']
            hash_name_file = hashlib.sha3_256(data[item]['id'].encode('utf-8'))
            hash_name_file = '\\' + hash_name_file.hexdigest() + '.jpg'
            if data[item]['image']:
                conn = requests.get(data[item]['image'], stream=True)
                with open(MEDIA_ROOT + '\somontj\phone' + hash_name_file, 'wb+') as file_down:
                    for chu in conn.iter_content(8192):
                        file_down.write(chu)
                somontjphone.image = MEDIA_ROOT + '\somontj\phone' + hash_name_file
            else:
                somontjphone.image = MEDIA_ROOT + '\photo.jpg'
            somontjphone.save()
        return