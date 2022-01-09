import os
import pytest
from django.conf import settings

@pytest.fixture(scope = "session")
def django_db_setup():
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(settings.BASE_DIR, "db.sqlite3"),
    }