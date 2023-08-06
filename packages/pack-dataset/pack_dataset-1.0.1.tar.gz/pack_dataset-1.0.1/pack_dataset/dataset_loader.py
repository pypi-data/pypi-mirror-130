import os
import pymssql
import pandas as pd


class GetterData:
    def __init__(self, username, password):
        self.connect_data = self.get_connect_data()
        self.connection = None
        if len(self.connect_data) > 0:
            self.connect_data['username'] = "GAZPROM-NEFT\\" + username
            self.connect_data['password'] = password
            self.connect_to_db()
        else:
            self.connect_data['username'] = "GAZPROM-NEFT\\" + username
            self.connect_data['password'] = password

    def get_connect_data(self):
        connect_data = {}
        try:
            connect_data_raw = os.environ.get(
                filter(lambda x: x.startswith("DATASET") and x.endswith("PATH"), os.environ).__next__())
            for pair in connect_data_raw.split(";")[:-1]:
                k, v = pair.split("=")
                connect_data[k.lower()] = v
        except Exception:
            print("Не удалось считать данные для подключения в автоматическом режиме введите их пожалуйста вручную!")
        return connect_data

    def connect_to_db(self):
        self.connection = pymssql.connect(self.connect_data["server"],
                                          self.connect_data["username"],
                                          self.connect_data["password"],
                                          self.connect_data["database"])

    def get_data_weather(self, row=0):
        if row:
            sql_query = f"SELECT TOP {row} * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        else:
            sql_query = f"SELECT * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        dataset = pd.read_sql(sql_query, self.connection)
        return dataset
