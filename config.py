import os

class Config(object):
    SECRET_KY = os.envorinment.get('SECRET_KEY') or "secret_string"