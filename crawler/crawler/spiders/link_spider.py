import scrapy
from bs4 import BeautifulSoup

class link_spider(scrapy.Spider):
    
    # scrapy crawl link_spider
    name = "link_spider"
    # product listing url, don't change name, can multiple, put in a list
    start_urls = [open("../../../cache/start_url.txt").read(), ]
    
    def parse(self,response):
        
        # the url will have one copy don't know why, use this toggle to eliminate
        odd = True 
        # a lot of html where we retrieve product_url_elements
        product = response.css('a.a-link-normal.a-text-normal').extract() 
        
        for item in zip(product):
            
            product_url_elements = (BeautifulSoup(item[0]).find('a', href=True)['href']).split("/") # a list splitting /smart-light-bulbs-alexa-wifi/dp/B08TB6VXFL/ref=sr_1_1?crid=29L7O275AMAW1&keywords=smart+light&qid=1681866990&sprefix=smart+li%2Caps%2C364&sr=8-1
            product_name = product_url_elements[1]
            product_dp = product_url_elements[2]
            product_code = product_url_elements[3]
            
            # to filter out some invalid product_url don't know why                
            if product_dp == "dp": 
                if odd:
                    link_1 = { # 1 star review page 1
                        'product_name': product_name.replace("-"," "),
                        'review_link': "https://www.amazon.com/" + product_name + "/product-reviews/" + product_code + "/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=one_star&pageNumber=1",}
                    link_2 = { # 1 star review page 2
                        'product_name': product_name.replace("-"," "),
                        'review_link': "https://www.amazon.com/" + product_name + "/product-reviews/" + product_code + "/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=one_star&pageNumber=2",}
                    yield link_1
                    yield link_2
                odd = not odd