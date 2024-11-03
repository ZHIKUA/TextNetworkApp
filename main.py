from flask import Flask
from controller.controller import home, analyze_data, craw_links, craw_reviews, generate_level_2, generate_level_3

app = Flask(
    __name__, 
    template_folder = "view", 
    static_folder="view/static"
)
app.config.update(dict(
    DEBUG=False,
    SEND_FILE_MAX_AGE_DEFAULT=0,
))

app.register_blueprint(home)
app.register_blueprint(analyze_data)
app.register_blueprint(craw_links)
app.register_blueprint(craw_reviews)
app.register_blueprint(generate_level_2)
app.register_blueprint(generate_level_3)

app.run()