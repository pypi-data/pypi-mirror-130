import os
import pymssql
import pandas as pd
from custom_exception import *
import hvac
import json


class GetterData:
    def __init__(self):
        self.connection = None
        self.connect_data = self.get_connect_data()
        self.settings = self.read_settings()

    def read_settings(self):
        with open("settings.json") as file:
            settings = json.load(file)
        return settings

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

    def connect_to_db_with_login(self, login, password):
        if len(self.connect_data) > 0:
            self.connect_data['username'] = self.settings['prefix_login'] + login
            self.connect_data['password'] = password
            self.connection = pymssql.connect(self.connect_data["server"],
                                              self.connect_data["username"],
                                              self.connect_data["password"],
                                              self.connect_data["database"])
        else:
            raise ConnectException

    def connect_to_db_with_token(self, vault_token, vault_secret_engine, vault_path):
        if len(self.connect_data) > 0:

            cli = hvac.Client(url= self.settings['url'],
                              token=vault_token, cert=(self.settings["cert_vault_tls"], self.settings["cert_vault_key"]),
                              verify=self.settings["cert_vault_verify"])
            if cli.is_authenticated():
                creds = cli.secrets.kv.v2.read_secret_version(mount_point=vault_secret_engine, path=vault_path).get(
                    "data").get("data")

                login = creds.get('username')
                password = creds.get('password')
                self.connect_data['username'] = self.settings['prefix_login'] + login
                self.connect_data['password'] = password
                self.connection = pymssql.connect(self.connect_data["server"],
                                                  self.connect_data["username"],
                                                  self.connect_data["password"],
                                                  self.connect_data["database"])
        else:
            raise ConnectException

    def get_data_weather(self, row=None):
        if (row is not None) and (type(row) == int) and (row > 0):
            sql_query = f"SELECT TOP {row} * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        elif type(row) != int or row < 0:
            raise RowException
        else:
            # Пока 35к как потолок, иначе кернел валится
            sql_query = f"SELECT TOP 35000 * FROM [{self.connect_data['database']}].[{self.connect_data['schema']}].[{self.connect_data['table']}]"
        dataset = pd.read_sql(sql_query, self.connection)
        return dataset
