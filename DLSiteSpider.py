# -*-coding: utf-8 -*-
# OOP rework @ 2020/2/3
# 获取一个月前发售的同人音声作品
# 获取销量榜单前10？
import os
import datetime

import requests
from bs4 import BeautifulSoup


class DLsite():
    def __init__(self):
        self.session = requests.session()
        self.header = {
            'Host': 'www.dlsite.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
        }
        self.imgHeader = {
            'Host': 'img.dlsite.jp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': 'image/webp,*/*',
            'Referer': 'https://www.dlsite.com/maniax/work/=/product_id/RJ274411.html'
        }
        # 使用前先勾选SS/SSR客户端中的允许局域网连接
        self.proxie = {
            'https': 'https://127.0.0.1:1078',
            'http': 'http://127.0.0.1:1078'
        }
        self.cookie = {
            'DL_SITE_DOMAIN': 'maniax',
            'dlsite_dozen': '9',
            'uniqid': '0.2wgxnlorlws',
            'adultchecked': '1'
        }
    def toAllowed(self,name):
        p = str(name)
        p = p.replace("/", "·").replace(":", "：").replace("*", "·")
        p = p.replace("?", "？").replace("\"", "'").replace("<", "《")
        p = p.replace(">", "》").replace("|", "·").replace("\\", "·")
        return p


    def mknewdir(self,foldername):
        if not os.path.exists(foldername):
            os.mkdir(foldername)

    def GetOneMonthAgoWorks(self):
        OneMonthAgo = (datetime.datetime.now() - datetime.timedelta(days=31)
                       ).strftime('%Y-%m-%d')  # Count one month as 31 days
        self.mknewdir(OneMonthAgo)
        url = f"https://www.dlsite.com/maniax/new/=/date/{OneMonthAgo}/work_type[0]/SOU/work_type[1]"
        
        req = self.session.get(url, headers=self.header, proxies=self.proxie)
        html = req.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        ThumbnailsList = []  # 作品封面缩略图链接
        for img in soup.find_all(name='img', attrs={'ref': 'popup_img'}):
            ThumbnailsList.append('https:' + img['src'])
        CoverList = list(map(lambda x: x.replace("resize", "modpub").replace(
            "_240x240.jpg", ".jpg"), ThumbnailsList))  # 作品封面大图链接
        
        for i, dt in enumerate(soup.find_all(name='dt', attrs={'class': 'work_name'})):
            for a in dt.find_all('a'):
                #print(a.string + '\n' + a.get('href'))S
                fp = os.path.join(OneMonthAgo,self.toAllowed(a.string.strip()))
                print(fp)
                self.mknewdir(fp)
                with open(os.path.join(fp, 'index.url'), 'w', encoding='utf-8') as f:
                    f.write('[InternetShortcut]\nurl=%s' % a.get('href'))
                r = requests.get(CoverList[i], headers=self.imgHeader, cookies=self.cookie, proxies=self.proxie)
                with open(os.path.join(fp, os.path.basename(CoverList[i])), 'wb') as f:
                    f.write(r.content)


if __name__ == '__main__':
    DL = DLsite()
    DL.GetOneMonthAgoWorks()
