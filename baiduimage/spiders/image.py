from scrapy import Selector
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import urllib.parse as urlparse
import json
import regex
import demjson
import urllib.request

class image(CrawlSpider):
    name = "baiduimage"
    start_urls = ['https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=色斑&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=色斑&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=0']

    def parse(self, response):
        html = json.loads(response.body_as_unicode())
        title = 'stain'
        for img in html.get('data'):
            if img.get('thumbURL'):
                di = img.get('di')
                url = img.get('thumbURL')
                #print(url)
                web = urllib.request.urlopen(url)
                data = web.read()
                with open('/home/liuzj/pyscrapy/py1/baiduimage/%s/%s.jpg' % (title, di), "wb") as f:
                    f.write(data)
                    f.close()
        metadict = response.meta
        page = metadict.get('page')
        if page:
            page = page + 30
        else:
            page = 30
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=色斑&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=色斑&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=%d' % (page)
        if page < 120:
            yield Request(url=url, meta={'page': page}, callback=self.parse)
        else:
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=素颜大头照&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=素颜大头照&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=0'
            yield Request(url=url, meta={'page': 30}, callback=self.parse_two)

    def parse_two(self, response):
        metadict = response.meta
        page = metadict.get('page')
        print(page)
        html = demjson.decode(response.body_as_unicode())
        title = 'face'
        for img in html.get('data'):
            if img.get('thumbURL'):
                di = img.get('di')
                url = img.get('thumbURL')
                print(url)
                web = urllib.request.urlopen(url)
                data = web.read()
                with open('/home/liuzj/pyscrapy/py1/baiduimage/%s/%s.jpg' % (title, di), "wb") as f:
                    f.write(data)
                    f.close()
        if page:
            page = page + 30
        else:
            page = 30
        url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=素颜大头照&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word=素颜大头照&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&cg=girl&pn=%d' % (page)
        if page < 120:
            print(url)
            yield Request(url=url, meta={'page': page}, callback=self.parse_two)
