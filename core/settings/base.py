import os
from core.configs import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'django-insecure-=x)ixlw6-2ln9th@#%c!9hoz=u^n2!1urw0h!$-8-4!=c=@4)#')

print('BASE_DIR:', BASE_DIR)
