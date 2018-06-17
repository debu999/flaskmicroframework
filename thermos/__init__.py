"""Thermos Application initialization package. This is a dummy placeholder."""
import socket
import sys
import os
from pprint import pprint as pp
import logging
from logging import Formatter, FileHandler
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from thermos.thermoscrypto.cryptostringgen import id_generator, staticid_generator
from flask_login import LoginManager
from flask_moment import Moment
basedir = os.path.abspath(os.path.dirname(__file__))
application = Flask(__name__)


# application.config['DEBUG'] = True

# Configure Database
application.config["SECRET_KEY"] = staticid_generator(hostname=socket.gethostname(),
                                                      ipaddr=socket.gethostbyname(socket.gethostname()),
                                                      dt=datetime.now().strftime("%d%B%Y"),
                                                      port="1247", flname=os.path.basename(__file__))
application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir,
                                                                            'thermos.db') + '?check_same_thread=False'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)
application.logger.setLevel(logging.DEBUG)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
# no login then redirect to login page
login_manager.login_view = "login"
login_manager.init_app(application)

#for displaying timestamps
moment = Moment(application)

import thermos.models
import thermos.views
