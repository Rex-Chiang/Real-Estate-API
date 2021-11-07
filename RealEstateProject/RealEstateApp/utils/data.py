from sqlalchemy import create_engine
from django.conf import settings
import pandas as pd
import os

class RealEstateData():
    def __init__(self, user, password):
        self.df = pd.read_csv ("./real_estate_data_csv/h_lvr_land_a.csv")
        self.user = user
        self.password = password

    def data_processing(self):
        self.df = self.df.drop([0])
        self.df = self.df.drop(columns = ["土地移轉總面積平方公尺", "都市土地使用分區", "非都市土地使用分區",
                                          "非都市土地使用編定", "主要用途", "主要建材",
                                          "建物現況格局-隔間", "車位類別", "備註",
                                          "編號", "主建物面積", "附屬建物面積",
                                          "陽台面積", "電梯", "移轉編號"])

        self.df["建物現況格局-房-廳-衛"] = self.df[["建物現況格局-房", "建物現況格局-廳", "建物現況格局-衛"]].apply('-'.join, axis = 1)
        self.df = self.df.drop(columns = ["建物現況格局-房", "建物現況格局-廳", "建物現況格局-衛"])

    def df_to_database(self):
        engine = create_engine("mysql+pymysql://" + self.user + ":" + self.password + "@localhost:3306/real_estate")
        self.df.to_sql(name = 'real_estate_taoyuan', con = engine, index = False)

if __name__ == "__main__":

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealEstateProject.settings')

    RealEstateData = RealEstateData(user = settings.DATABASES["real_estate_db"]["USER"],
                                    password = settings.DATABASES["real_estate_db"]["PASSWORD"])
    RealEstateData.data_processing()
    RealEstateData.df_to_database()