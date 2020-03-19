# -*- encoding: utf-8 -*-
from .settings import MYSQL_DBNAME, MYSQL_HOST, MYSQL_PASSWD, MYSQL_PORT, MYSQL_USER

from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker

mysql_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{dbname}?charset=utf8'.format(
    user=MYSQL_USER,
    password=MYSQL_PASSWD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    dbname=MYSQL_DBNAME)

engine = create_engine(
    mysql_url,
    pool_size=20,
    max_overflow=0,
    echo=False)
DB_Session = sessionmaker(bind=engine)


class SessionMysql:

    def __init__(
            self,
            data=None,
            tablename=None,
            create_sql=None,
            sql_statement=None):
        self.sql_statement = sql_statement  # 自定义sql
        self.create_sql = create_sql  # 创建sql语句
        self.tablename = tablename  # 数据库名
        self.keys = self.data_k_v(data, 0)
        self.values = self.data_k_v(data, 1)
        # self.engine = create_engine('mysql+pymysql://root:12345678@127.0.0.1:3306/spider?charset=utf8',echo=False)
        # echo控制是否打印sql语言，True为打印
        # 创建会话类
        # self.DB_Session = sessionmaker(bind=engine)
        # 创建会话对象
        # self.session = self.DB_Session()

    def data_k_v(self, data, index):
        """
        将字典key和value分离成字符串,当index = 0 时获取key，当index=1时获取value
        :param data:字典类型
        :return:str
        """
        if data is not None and data != {}:
            if index == 0:
                keys = ",".join(data.keys())
                # keys = tuple(data.keys())
                return keys
            if index == 1:
                # values = ",".join(str(x) for x in data.values())
                values_1 = tuple(data.values())
                values = str(values_1).replace("[]", " \'\' ")
                return values
        else:
            return None

    def execute_sql(self, action=""):
        """
        数据库操作，目前支持自定义(为空)，插入(insert)和删除(delete)
        :param action:
        "":执行自己传入sql语句(sql_statement)
        insert:执行insert语句
        delete：执行insert语句
        :return:
        """
        with engine.connect() as connection:
            trans = connection.begin()
            try:

                if action == "insert":
                    sql_operating = self.insert_sql()
                    connection.execute(sql_operating)
                if action == "delete":
                    sql_operating = self.delete_sql()
                    for i in sql_operating:
                        connection.execute(sql_operating)
                if action == "":
                    sql_operating = self.sql_statement
                    connection.execute(sql_operating)
                trans.commit()
            except Exception as e:
                trans.rollback()  # 回滚事务
                print("执行sql操作失败：" + e)

        # 用完记得关闭，也可以用with

    def is_redundant(self, select_sql=None):
        """
        检查数据库是否重复
        :param:数据库语句
        :return:
        """
        if select_sql is not None:

            session = DB_Session()
            selete_data = session.execute(select_sql).fetchall()
            session.close()
            return selete_data
        else:
            return 0

    def insert_sql(self):
        """
        插入语句
        :return:str
        """
        if self.keys is not None and self.values is not None:
            insert_sql = "insert into {0}({1}) value{2}".format(
                self.tablename, self.keys, self.values)
            return insert_sql
        else:
            return None

    def delete_sql(self):
        """
        TODO:这里的keys和value只能是字符串，后期需要修改
        删除语句
        :return:list
        """
        if self.keys is not None and self.values is not None:
            key_arr = self.keys.spilt(",")
            value_arr = self.values.split(",")
            delete_sqls = []
            for i in key_arr.__len__():
                delete_sql = "delete from {0} where {1}={2}".format(
                    self.tablename, key_arr[i], value_arr[i])
                delete_sqls.append(delete_sql)
            return delete_sqls
        else:
            return None

    def update(self):
        pass

    def close(self, session):
        """关闭会话"""
        return session.close()

    def select_districts_info(self, select_sql):
        """
        获取城市列表
        :param tablename:
        :return: array
        """
        session = DB_Session()
        sql_data = session.execute(select_sql).fetchall()
        new_data = []
        for data in sql_data:
            new_data.append(data[0])
        return new_data


# ModelBase.metadata.create_all(engine)
if __name__ == "__main__":
    # select_sql = "select gaode_id from resource_info where gaode_id = 'B0FFIPVFG4'"
#     # sessionmysql = SessionMysql(tablename="resource_info").is_redundant(select_sql)
#     # print(sessionmysql)
    sessionmysql = SessionMysql(tablename="districts_info")
    select_sql = "SELECT DISTINCT city_name FROM `districts_info` where province_name ='福建省'"
    city = sessionmysql.select_districts_info(select_sql)
    # print(city)