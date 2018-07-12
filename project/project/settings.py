SECRET_KEY = '3_=m+0v!u=*wmgxf7yo8*4zlblkxv19#jzu3ns!1bibyzr+td^'
ALGORITHM = 'HS256'
EXPIRY_TIME = 360

DATABASES = {
    'default': {
        'NAME':'apistar',
        'HOST': 'localhost',
        'PORT': 27017,
        'USERNAME': '',
        'PASSWORD': ''
    }
}

ORIGIN = '*'

NO_AUTH_ENDPOINTS = ['/login', '/docs']
