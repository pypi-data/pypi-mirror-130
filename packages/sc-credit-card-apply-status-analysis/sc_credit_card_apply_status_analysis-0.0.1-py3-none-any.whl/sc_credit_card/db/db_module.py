#  The MIT License (MIT)
#
#  Copyright (c) 2021. Scott Lau
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from config42 import ConfigManager
from mysqlhelper import MySQLHelper
from sc_utilities import Singleton


class DBModule(metaclass=Singleton):
    """
    数据库操作模块
    """

    def __init__(self, *, config: ConfigManager):
        self._config = config
        # 数据库相关配置
        self._db_host = config.get("database.host")
        self._db_port = config.get("database.port")
        self._db_database = config.get("database.database")
        self._db_user = config.get("database.user")
        self._db_password = config.get("database.password")
        self._db_helper = MySQLHelper(
            host=self._db_host,
            port=self._db_port,
            user=self._db_user,
            password=self._db_password,
            database=self._db_database,
        )

    def select_one(self, *, sql, param=()):
        return self._db_helper.select_one(sql=sql, param=param)

    def select_all(self, *, sql, param=()):
        return self._db_helper.select_all(sql=sql, param=param)

    def execute(self, *, sql, param=(), auto_close=False):
        return self._db_helper.execute(sql=sql, param=param, auto_close=auto_close)
