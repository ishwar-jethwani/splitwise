import os
DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ["SECRET_KEY"]
SERVER = os.environ["SERVER"]

# Database Connection
HOST = os.environ.get("HOST", "db")
PORT = int(os.environ.get("PORT", default="5432"))
NAME = os.environ.get("NAME")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")

# Admin os.environ.geturation
ADMIN_SITE_HEADER = os.environ.get("ADMIN_SITE_HEADER")

# Email os.environ.getuaration
EMAIL_HOST_USER_NAME = os.environ.get("EMAIL_HOST_USER_NAME")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
