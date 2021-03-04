import os


VERSION = '0.1.0'
TITLE = 'Ratatouille'
DEBUG = os.getenv('DEBUG') == 'true'

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')
