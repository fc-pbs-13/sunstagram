from .base import *

ENV = 'DevTest'

TEST = True

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
