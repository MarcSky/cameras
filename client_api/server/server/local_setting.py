

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'OPTIONS': {
            'options': '-c search_path=api,public'
        },
        'HOST': 'localhost',
        'PORT': '5432',
        'NAME': 'demo_db',
        'USER': 'tosha',
        'PASSWORD': 'qwerty12+',
    },
}