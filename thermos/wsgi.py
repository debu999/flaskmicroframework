"""WSGI python file for more running flask app with gunicorn"""
from thermos.thermos import application

if __name__ == "__main__":
    application.run()
