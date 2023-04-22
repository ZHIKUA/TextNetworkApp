import scrapy
import pandas as pd
from bs4 import BeautifulSoup

class review_spider(scrapy.Spider):
    
    name = "review_spider"
    start_urls = list(pd.read_excel("../../../cache/link.xlsx")["review_link"])
    
    def parse(self,response):
        product_name = response.url.split("/")[3].replace("-"," ")
        review_titles = response.css('.review-title').extract()
        review_texts = response.css('.review-text').extract()
        for item in zip(review_titles,review_texts):
            review = {
                'product_name': product_name,
                'title': BeautifulSoup(item[0]).text,
                'review': BeautifulSoup(item[1]).text[1:]} # to escape the \n at [0]
            yield review
