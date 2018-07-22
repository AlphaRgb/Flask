#!/usr/bin/env python3
# coding=utf-8

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .proxy import proxy as proxy_blueprint
    app.register_blueprint(proxy_blueprint)

    from .novel import novel as novel_blueprint
    app.register_blueprint(novel_blueprint)

    from .cnn import cnn as cnn_blueprint
    app.register_blueprint(cnn_blueprint)

    from .resume import resume as resume_blueprint
    app.register_blueprint(resume_blueprint)

    return app
