import configparser
config = configparser.ConfigParser()

config.read('config.ini')
try:
    DJANGO_SECRET_KEY = config['django']['SECRET_KEY']
    LOCAL_DB_USER = config['django']['DB_USER']
    LOCAL_DB_PASS = config['django']['DB_PASS']
except KeyError:
    DJANGO_SECRET_KEY = ''
    LOCAL_DB_USER = ''
    LOCAL_DB_PASS = ''

