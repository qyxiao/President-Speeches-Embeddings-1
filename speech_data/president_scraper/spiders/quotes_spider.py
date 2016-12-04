"""quoteS_spider.py"""

__author__ = 'bharathipriyaa'


import scrapy
import csv
import os
from scrapy.selector import Selector

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    url = "http://millercenter.org"
    start_urls = [
        'http://millercenter.org/president/speeches'
    ]


    def parse(self, response):

        # extract all links from page
        all_links = response.xpath('*//a/@href').extract()
        # iterate over links
        for link in all_links:
            if(link != "#top"):
                token = link.split('/')
                if(len(token) > 2) and link.find("speeches") != -1 :
                    president_name  = token[2]
                    file_name = token[len(token) - 1]
                    request = scrapy.Request(response.urljoin(link),
                                         callback=self.parse_speech)
                    request.meta['president'] = president_name
                    request.meta['file'] = file_name
                    yield request
    def parse_speech(self, response):
        president_name = response.meta['president']

        alltext = ''.join(response.xpath("*//div[@id='transcript']/p/text()").extract())
        print(alltext)
        file_name = "data/" + president_name +"/" + response.meta['file'] + ".txt"
        print(file_name)
        if not os.path.exists(os.path.dirname(file_name)):
            try:
                os.makedirs(os.path.dirname(file_name))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_name, "w") as f:
            f.write(alltext)
        print("Saved speech {}".format(file_name))



    def parse_old(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        # iterate over links
        with open('names.csv', 'w') as csvfile:
            fieldnames = ['Name', 'Link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for link in all_links:
                if(link != "#top"):
                    token = link.split('/')
                    if(len(token) > 2) and link.find("speeches") != -1 :
                        print("Link --> {}".format(link))
                        writer.writerow({'Name': token[2], 'Link': self.url+link})

