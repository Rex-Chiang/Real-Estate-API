from django.conf import settings
from django.db import connections
from django.db.utils import OperationalError
import subprocess

if settings.DEBUG:
    # If MySQL server hasn't connect, use another process to connect
    try:
        mysql_db = connections["real_estate_db"]
        # Will raise the exception if have connected problem
        mysql_db.ensure_connection()
        print("External MySQL Database Connected !")
    except OperationalError as msg:
        print(msg)
        print("Wait For Connecting ...")

        process = subprocess.Popen("mysqld",
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        print("External MySQL Database Connected !")