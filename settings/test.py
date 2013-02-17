"""Local test settings and globals which allows us to run our
test suite locally."""

from .base import *
########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = PROJECT_DIR
TEST_DISCOVER_ROOT = PROJECT_DIR
TEST_DISCOVER_PATTERN = "*"
########## IN-MEMORY TEST DATABASE
DATABASES = {
"default": {
"ENGINE": "django.db.backends.sqlite3",
"NAME": ":memory:",
"USER": "",
"PASSWORD": "",
"HOST": "",
"PORT": "",
},
}
