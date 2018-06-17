"""WSGI python file for more running flask app with gunicorn"""
import sys
from pprint import pprint as pp

from thermos.views import application

if __name__ == "__main__":
    application.run(debug=True)
