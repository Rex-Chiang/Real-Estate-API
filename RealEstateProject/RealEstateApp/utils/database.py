from django.conf import settings
import pymysql

class ControlExternalDB():
    def __init__(self):
        self.db = pymysql.connect(user = settings.DATABASES["real_estate_db"]["USER"],
                                  password = settings.DATABASES["real_estate_db"]["PASSWORD"],
                                  host = settings.DATABASES["real_estate_db"]["HOST"],
                                  port = int(settings.DATABASES["real_estate_db"]["PORT"]),
                                  db = settings.DATABASES["real_estate_db"]["NAME"],
                                  cursorclass = pymysql.cursors.DictCursor)
    def query(self, command):
        cursor = self.db.cursor()
        cursor.execute(command)
        data = cursor.fetchall()
        self.db.close()
        return data