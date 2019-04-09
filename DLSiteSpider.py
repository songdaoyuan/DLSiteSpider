# -*-coding: utf-8 -*-
import os
import requests
import datetime
from bs4 import BeautifulSoup


def toAllowed(name):
    p = str(name)
    p = p.replace("/", "·").replace(":", "：").replace("*", "·")
    p = p.replace("?", "？").replace("\"", "'").replace("<", "《")
    p = p.replace(">", "》").replace("|", "·").replace("\\", "·")
    return p


def mknewdir(foldername):
    if not os.path.exists(foldername):
        os.mkdir(foldername)


def getRawImgSrc(imgsrc):
    seq = ('https:', imgsrc.replace("resize", "modpub").replace("_240x240.jpg", ".jpg"))
    return "".join(seq)


OneMonthAgo = (datetime.datetime.now() - datetime.timedelta(days=31)
               ).strftime('%Y-%m-%d')  # Count one month as 31 days

url = 'https://www.dlsite.com/maniax/new/=/date/%s/work_type[0]/SOU/work_type[1]' % OneMonthAgo

mknewdir(OneMonthAgo)

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Referer': 'https://www.dlsite.com/maniax/',
    'Origin': 'https://www.dlsite.com'
}

cookie = {
    'adultchecked': '1',
    '_jp_user': '1',
    'lang': 'ja'
}

r = requests.get(url, headers=header, cookies=cookie)
html = r.content.decode('utf-8')

soup = BeautifulSoup(html, 'lxml')

srcList = []
for img in soup.find_all(name='img', attrs={'ref': 'popup_img'}):
    srcList.append(getRawImgSrc(img['src']))


for i, dt in enumerate(soup.find_all(name='dt', attrs={'class': 'work_name'})):
    for a in dt.find_all('a'):
        #print(a.string + '\n' + a.get('href'))
        fp = os.path.join(OneMonthAgo, toAllowed(a.string.strip()))
        print(fp)
        mknewdir(fp)
        with open(os.path.join(fp, 'index.url'), 'w', encoding='utf-8') as f:
            f.write('[InternetShortcut]\nurl=%s' % a.get('href'))
        r = requests.get(srcList[i], headers=header, cookies=cookie)
        with open(os.path.join(fp, os.path.basename(srcList[i])), 'wb') as f:
            f.write(r.content)

print('Done')
