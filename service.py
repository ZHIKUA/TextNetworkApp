import os
import json
import utility
import pandas as pd

def crawl_link(product_name):
    start_url = "https://www.amazon.com/s?k=" + product_name
    open("cache/start_url.txt", "w").write(start_url)
    os.chdir("crawler/crawler/spiders")
    os.system("scrapy crawl link_spider -O ../../../cache/link.xlsx")
    os.chdir("../../..") # otherwise will stay there
    
def crawl_review():
    os.chdir("crawler/crawler/spiders")
    os.system("scrapy crawl review_spider -O ../../../cache/review.xlsx")
    os.chdir("../../..")

def get_level_2(level_1):
    print("reading file...")
    reviews = list(pd.read_excel("cache/review.xlsx")["review"])
    print("preprocessing text data...")
    reviews = utility.preprocess(reviews, level_1)
    print("drawing network...")
    network = utility.get_network(reviews, level_1)
    print("calculating centralities...")
    network.to_excel("cache/network.xlsx", index=False)
    level_2 = utility.get_eigenvector_centralities(network)
    json.dump(level_2, open('cache/level_2.json', 'w'))    
    print("results returned")
    return level_2

def get_network(chosen_nodes):
    network = pd.read_excel("cache/network.xlsx")
    simplified_network = utility.simplify_network(network, chosen_nodes)
    fig = utility.visualize_network(simplified_network)
    fig.savefig("view/static/network.jpg")

if __name__ == "__main__":
    # stage 1
#    crawl_link("robot vacuum")
#    crawl_review()
    
    # stage 2
#    level_2 = get_level_2("watch")
#    print(level_2)

    # stage 3
    chosen_nodes = ["unfrozen", "fat", "profit", "rubbery"]
    get_network(chosen_nodes)