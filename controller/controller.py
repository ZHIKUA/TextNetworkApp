import json
import service.service as service
from flask import render_template, Blueprint, request, redirect

home = Blueprint("home", __name__)
analyze_data = Blueprint("analyze_data", __name__)
craw_links = Blueprint("craw_links", __name__)
craw_reviews = Blueprint("craw_reviews", __name__)
generate_level_2 = Blueprint("generate_level_2", __name__)
generate_level_3 = Blueprint("generate_level_3", __name__)

@home.route("/")
def index():
    return render_template("home.html")

@analyze_data.route("/analyze_data")
def analyze_data_controller():
    level_2 = json.load(open('cache/level_2.json', 'r'))
    return render_template("analyze_data.html", level_2=level_2)

@craw_links.route("/craw_links", methods=["POST"])
def craw_links_controller():
    product_name = request.form.get("product_name").replace(" ","+")
    service.crawl_link(product_name)
    return redirect("home.html")

@craw_reviews.route("/craw_reviews", methods=["POST"])
def craw_reviews_controller():
    service.crawl_review()
    return redirect("analyze_data.html")

@generate_level_2.route("/generate_level_2", methods=["POST"])
def generate_level_2_controller():
    level_1 = request.form.get("level_1")
    service.get_level_2(level_1) # i suppose it's written to file
    return redirect("analyze_data.html")

@generate_level_3.route("/generate_level_3", methods=["POST"])
def generate_level_3_controller():
    chosen_nodes = request.form.getlist("chosen_nodes")
    service.get_network(chosen_nodes) # i suppose level_1 node can be referred
    return redirect("analyze_data.html")