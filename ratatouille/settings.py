import os


VERSION = '0.1.0'
TITLE = 'Ratatouille'
DEBUG = os.getenv('DEBUG') == 'true'
ENVIRONMENT = os.getenv('ENVIRONMENT')
IS_PRODUCTION = ENVIRONMENT == 'production'

ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS').split(',')

DATABASES = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('POSTGRES_HOST'),
                'port': os.getenv('POSTGRES_PORT'),
                'user': os.getenv('POSTGRES_USER'),
                'password': os.getenv('POSTGRES_PASSWORD'),
                'database': os.getenv('POSTGRES_DB'),
            },
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', 'ratatouille.models'],
            'default_connection': 'default',
        }
    }
}

TEST_DATABASES = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.getenv('POSTGRES_HOST'),
                'port': os.getenv('POSTGRES_PORT'),
                'user': os.getenv('POSTGRES_USER'),
                'password': os.getenv('POSTGRES_PASSWORD'),
                'database': os.getenv('POSTGRES_DB_TEST'),
            },
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models', 'ratatouille.models'],
            'default_connection': 'default',
        }
    }
}

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_PORT = os.getenv("ELASTICSEARCH_PORT")
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': f'{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}'
    },
}

GANDALF_LOGIN_URL = os.getenv('GANDALF_LOGIN_URL')
GANDALF_ME_URL = os.getenv('GANDALF_ME_URL')
