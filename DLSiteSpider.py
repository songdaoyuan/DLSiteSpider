# -*-coding: utf-8 -*-
# OOP rework @ 2020/2/3
#Multi-Thread Download rework @ 2020/2/6
# 获取一个月前发售的同人音声作品
# 获取销量榜单前10？
import concurrent
import datetime
import os
import time
from concurrent.futures import ThreadPoolExecutor

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
            'Referer': 'https://www.dlsite.com/maniax/'
        }
        # 使用前先勾选SS/SSR客户端中的允许局域网连接或启用全局代理
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

    def GetOneMonthAgoWorks(self):
        def toAllowed(name):
            p = str(name)
            p = p.replace("/", "·").replace(":", "：").replace("*", "·")
            p = p.replace("?", "？").replace("\"", "'").replace("<", "《")
            p = p.replace(">", "》").replace("|", "·").replace("\\", "·")
            return p

        def mknewdir(foldername):
            if not os.path.exists(foldername):
                os.mkdir(foldername)

        self.OneMonthAgo = (datetime.datetime.now() - datetime.timedelta(days=31)
                            ).strftime('%Y-%m-%d')  # Count one month as 31 days
        mknewdir(self.OneMonthAgo)
        url = f"https://www.dlsite.com/maniax/new/=/date/{self.OneMonthAgo}/work_type[0]/SOU/work_type[1]"

        req = self.session.get(url, headers=self.header, proxies=self.proxie)
        html = req.content.decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')
        self.ThumbnailsList = []  # 作品封面缩略图链接
        self.TitleList = []  # 作品标题名
        self.UrlList = []  # 作品链接

        for img in soup.find_all(name='img', attrs={'ref': 'popup_img'}):
            self.ThumbnailsList.append('https:' + img['src'])

        self.CoverList = list(map(lambda x: x.replace("resize", "modpub").replace(
            "_240x240.jpg", ".jpg"), self.ThumbnailsList))  # 作品封面大图链接

        for dt in soup.find_all(name='dt', attrs={'class': 'work_name'}):
            for a in dt.find_all('a'):
                self.TitleList.append(toAllowed(a.string.strip()))
                self.UrlList.append(a.get('href'))
        self.MTDownload(self.CoverList, self.TitleList, self.UrlList)
        '''
                fp = os.path.join(OneMonthAgo,toAllowed(a.string.strip()))
                print(fp)
                self.mknewdir(fp)
                with open(os.path.join(fp, 'index.url'), 'w', encoding='utf-8') as f:
                    f.write('[InternetShortcut]\nurl=%s' % a.get('href'))
                r = requests.get(CoverList[i], headers=self.imgHeader, cookies=self.cookie, proxies=self.proxie)
                with open(os.path.join(fp, os.path.basename(CoverList[i])), 'wb') as f:
                    f.write(r.content)
        '''

    def MTDownload(self, CList, TList, UList):
        with concurrent.futures.ProcessPoolExecutor(max_workers=8) as exector:
            for c, t, u in zip(CList, TList, UList):
                exector.submit(self.download, c, t, u)
        '''
        删除注释并且注释上面的代码块来启用单线程下载
        for c,t,u in zip(CList,TList,UList):
            self.download(c,t,u)
        '''

    def download(self, cover, title, url):
        fp = os.path.join(self.OneMonthAgo, title)
        imgp = os.path.join(fp, os.path.basename(cover))
        urlp = os.path.join(fp, 'index.url')
        r = requests.get(cover, headers=self.imgHeader,
                         cookies=self.cookie, proxies=self.proxie)
        if not os.path.exists(fp):
            os.mkdir(fp)
        with open(imgp, 'wb') as f:
            f.write(r.content)
        with open(urlp, 'w', encoding='utf-8') as f:
            f.write(f'[InternetShortcut]\nurl={url}')


if __name__ == '__main__':
    t1 = time.perf_counter()
    DL = DLsite()
    DL.GetOneMonthAgoWorks()
    t2 = time.perf_counter()
    print(t2-t1)
