import os
import pandas as pd
import util.utility as utility

def crawl_link(product_name):
    start_url = "https://www.amazon.com/s?k=" + product_name
    open("cache/start_url.txt", "w").write(start_url) # need to pass start_url to scrapy in this way
    os.chdir("crawler/crawler/spiders")
    os.system("scrapy crawl link_spider -O ../../../cache/link.xlsx")
    os.chdir("../../..")
    
def crawl_review():
    os.chdir("crawler/crawler/spiders")
    os.system("scrapy crawl review_spider -O ../../../cache/review.xlsx")
    os.chdir("../../..")

def get_level_2(level_1):
    if not level_1: return
    print("reading file...")
    reviews = list(pd.read_excel("cache/review.xlsx")["review"])
    print("preprocessing text data...")
    reviews = utility.preprocess(reviews, level_1)
    print("drawing network...")
    network = utility.get_network(reviews, level_1)
    network.to_excel("cache/network.xlsx", index=False)
    utility.save_network_graph(network)
    print("calculating centralities...")
    level_2 = utility.get_eigenvector_centralities(network)
    print("results returned")    
    return level_2

def get_level_3(level_2):
    network = pd.read_excel("cache/network.xlsx")
    simplified_network = utility.simplify_network(network, level_2)
    return simplified_network