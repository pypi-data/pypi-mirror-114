import pandas as pd
import pymysql


class MysqlPool:

    def __init__(self, config):
        self._conn = pymysql.connect(**config)

    def fetch_data(self, sql):
        data = pd.read_sql(sql, self._conn)
        return data

    def execute_sql(self, sql):
        cursor = self._conn.cursor()
        cursor.execute(sql)
        self._conn.commit()

    def insert_df(self, table, df):
        cols = "(`{}`)".format("`,`".join(df.columns.to_list()))
        value_list = []
        for idx, row in df.iterrows():
            v = tuple(row.to_list())
            value_list.append(str(v))
        values = ",".join(value_list)
        sql = "INSERT INTO {} {} VALUES {}".format(table, cols, values)
        self.execute_sql(sql)

    def close(self):
        if self._conn:
            self._conn.close()
