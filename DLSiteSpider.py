# -*-coding: utf-8 -*-
import os
import requests
import datetime
from bs4 import BeautifulSoup
'''
https://img.dlsite.jp/resize/images2/work/doujin/RJ248000/RJ247307_img_main_240x240.jpg
https://img.dlsite.jp/modpub/images2/work/doujin/RJ248000/RJ247307_img_main.jpg
'''

def toAllowed(name):
    p = str(name)
    p = p.replace("/", "·").replace(":", "：").replace("*", "·")
    p = p.replace("?", "？").replace("\"", "'").replace("<", "《")
    p = p.replace(">", "》").replace("|", "·").replace("\\", "·")
    return p


def mknewdir(foldername):
    if not os.path.exists(foldername):
        os.mkdir(foldername)


url = 'https://www.dlsite.com/maniax/new/=/date/2019-02-27/work_type[0]/SOU/work_type[1]'
OneMonthAgo = (datetime.datetime.now() - datetime.timedelta(days=31)
               ).strftime('%Y.%m.%d')  # Count one month as 31 days

mknewdir(OneMonthAgo)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Referer': 'https://www.dlsite.com/maniax/',
    'Origin': 'https://www.dlsite.com'
}

Cookie = {
    'adultchecked': '1',
    '_jp_user': '1',
    'lang': 'ja'
}

#r = requests.get(url, headers = header, cookies = Cookie)
#html = response.content.decode('utf-8')
with open('cache.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'lxml')

for dt in soup.find_all(name='dt', attrs={'class': 'work_name'}):
    for a in dt.find_all('a'):
        #print(a.string + '\n' + a.get('href'))
        mknewdir(OneMonthAgo + '/' + toAllowed(a.string.strip()))