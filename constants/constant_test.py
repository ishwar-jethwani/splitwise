from decouple import config

# Created On 28-11-2022 at 15:21
# Debug Mode
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY")
SERVER = config("SERVER", default=True, cast=bool)
HOST = config("HOST", default="db")
PORT = int(config("PORT", default="5432"))
NAME = config("NAME")
USER = config("USER")
PASSWORD = config("PASSWORD")

# Admin Configuration
ADMIN_SITE_HEADER = config("ADMIN_SITE_HEADER")

# Email Configuaration
EMAIL_HOST_USER_NAME = config("EMAIL_HOST_USER_NAME")
EMAIL_PASSWORD = config("EMAIL_PASSWORD")
OPEN_AI_KEY = config("OPEN_AI_KEY")
REDIS_HOST = config("REDIS_HOST")

# PAYMENT
PAYMENT_TEST_ID = config("PAYMENT_TEST_ID")
PAYMENT_TEST_SECRET = config("PAYMENT_TEST_SECRET")
