import json
import service
from flask import render_template, Blueprint, request

home = Blueprint("home", __name__)
stage_1 = Blueprint("stage_1", __name__)
stage_2 = Blueprint("stage_2", __name__)
stage_3 = Blueprint("stage_3", __name__)

@home.route("/")
def index():
    return render_template("home.html")

@stage_1.route("/stage_1")
def stage1():
    product_name = request.args.to_dict().get("product_name").replace(" ","+")
    service.crawl_link(product_name)
    return render_template("stage_1.html")

@stage_2.route("/stage_2")
def stage2():
    is_reselect = request.args.to_dict().get("is_reselect")
    if not is_reselect: # navigating from stage_1
        service.crawl_review()
    # else navigating from stage_3
    return render_template("stage_2.html")

@stage_3.route("/stage_3", methods=["GET","POST"])
def stage3():
    level_1 = request.args.to_dict().get("level_1")
    chosen_nodes = request.form.getlist("chosen_nodes")
    if not chosen_nodes: # navigating from stage_2
        level_2 = service.get_level_2(level_1)
    else: # nodes chosen and then generate network graph
        level_2 = json.load(open('cache/level_2.json', 'r'))
        service.get_network(chosen_nodes)
    return render_template("stage_3.html", level_1=level_1, level_2=level_2, chosen_nodes=chosen_nodes)
