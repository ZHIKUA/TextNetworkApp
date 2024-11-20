import json
import util.utility as utility
import service.service as service
from flask import render_template, Blueprint, request, redirect, url_for

home = Blueprint("home", __name__)
analyze_data = Blueprint("analyze_data", __name__)
crawl_links = Blueprint("crawl_links", __name__)
crawl_reviews = Blueprint("crawl_reviews", __name__)
generate_level_2 = Blueprint("generate_level_2", __name__)
generate_level_3 = Blueprint("generate_level_3", __name__)

@home.route("/")
def index():
    return render_template("home.html")

@analyze_data.route("/analyze_data")
def analyze_data_controller():
    level_1 = request.args.get('level_1', '')
    level_2 = json.load(open('cache/level_2.json', 'r')) if level_1 else {}
    return render_template("analyze_data.html", level_1=level_1, level_2=level_2, chosen_nodes=request.args.getlist('chosen_nodes'))

@crawl_links.route("/crawl_links", methods=["POST"])
def crawl_links_controller():
    product_name = request.form.get("product_name").replace(" ","+")
    service.crawl_link(product_name)
    return redirect("home")

@crawl_reviews.route("/crawl_reviews", methods=["POST"])
def crawl_reviews_controller():
    service.crawl_review()
    return redirect("analyze_data")

@generate_level_2.route("/generate_level_2", methods=["POST"])
def generate_level_2_controller():
    level_1 = request.form.get("level_1")
    level_2 = service.get_level_2(level_1)
    json.dump(level_2, open('cache/level_2.json', 'w'))
    return redirect(url_for("analyze_data.analyze_data_controller", level_1=level_1))

@generate_level_3.route("/generate_level_3", methods=["POST"])
def generate_level_3_controller():
    chosen_nodes = request.form.getlist("chosen_nodes")
    network = service.get_level_3(chosen_nodes)
    utility.save_network_graph(network)
    return redirect(url_for("analyze_data.analyze_data_controller", chosen_nodes=chosen_nodes, level_1=request.form.get("level_1")))