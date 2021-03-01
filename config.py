import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'*,\x86\x14\xb1\x1e\x14qy\xe4B\xbc\x07\xc1B\xda'

    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }
