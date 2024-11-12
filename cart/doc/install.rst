1. create app -> python -m manage startapp cartService
2. install rest framework -> pip install djangorestframework
    INSTALLED_APPS = [
    'rest_framework',
    ]

    # settings.py

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
    }

3. install mysql -> pip install mysqlclient
    in setting overwrite code
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.mysql",
                "NAME": "cartservice",
                "USER": 'root',
                "PASSWORD": 'Deepa@123',
                "HOST": '127.0.0.1',
                "PORT": '3306',
            }
        }
