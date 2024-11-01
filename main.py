from flask import Flask
from controller.controller import home, stage_1, stage_2, stage_3

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
app.register_blueprint(stage_1)
app.register_blueprint(stage_2)
app.register_blueprint(stage_3)

app.run()