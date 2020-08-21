import MySQLdb
import traceback
from Db.BuildSql import BuildSql

class DB:
    '数据库操作'

    def __init__(self, host, username, password, dbname, port = 3306, charset='utf8', options={}):
        self.host = host
        self.username = username
        self.password = password
        self.dbname = dbname
        self.port = port
        self.charset = charset
        self.options = options
        self._initData()


    def _initData(self):
        self.sql = ''
        self.db = None
        self.cursor = None
        self.sqlBuilder = None


    # 链接数据库
    def _connect(self):
        if self.db is None or not self.db:
            self.db = MySQLdb.connect(
                host=self.host,
                user= self.username,
                password = self.password,
                db = self.dbname,
                charset = self.charset,
                port = self.port,
            )

        return self.db

    # 获取游标
    def _getCursor(self):
        if not self.cursor or self.cursor is None:
            self.cursor = self._connect().cursor()
        return self.cursor

    # 执行sql
    def excute(self, sql = ''):
        print(self.sql)
        if not sql is None:
            if self.sql is None:
                print('over')
                return 0
            sql = self.sql
        print(sql)
        cursor = self._getCursor()
        print('asdf',cursor)
        cursor.execute(sql)
        return cursor

    def _getBuilder(self):
        if not self.sqlBuilder or self.sqlBuilder is None:
            self.sqlBuilder = BuildSql()
        return self.sqlBuilder


    def table(self, tableName):
        self._getBuilder().table(tableName)
        return self

    def alias(self, aliasName):
        self._getBuilder().alias(aliasName)
        return self

    def join(self, tableName, primaryKey, operate = '=', foreignKey = '', type='left'):
        self._getBuilder().join(tableName,primaryKey,operate, foreignKey, type)
        return self

    # 添加
    def where(self, column, operate = '', value = ''):
        self._getBuilder().where(column, operate, value)
        return self

    def orWhere(self, column, operate = '', value = ''):
        self._getBuilder().orWhere(column, operate, value)
        return self

    # having(subSql)
    def having(self, subSql, relation = 'and'):
        self._getBuilder().having(subSql, relation)
        return self


    # select fields
    def select(self, fields = []):
        self._getBuilder().select(fields)
        return self

    # order by
    def orderBy(self, column, order='asc'):
        self._getBuilder().orderBy(column,order)
        return self

    # group by 字段
    def groupBy(self, column):
        self._getBuilder().groupBy(column)
        return self

    # limit限制
    def limit(self, length, offset=0):
        self._getBuilder().limit(length,offset)
        return self

    # 字典排序
    def dictSort(self, dictData):
        data = {}
        for i in sorted(dictData):
            data[i] = dictData[i]
        return data

    # 插入单条数据
    def _insertOne(self, data):
        data = self.dictSort(data);
        if not self.sql or self.sql is None:
            self.sql = self._getBuilder().formatData(data).operater('insert').buildSql()
        sql = self.sql % tuple(data.values())
        self._getCursor().execute(sql)
        return self._getCursor().lastrowid;

    # 插入数据
    def insert(self, data):
        try:
            if isinstance(data, dict):
                res = self._insertOne(data)
            elif isinstance(data, list):
                while len(data):
                    item = data.pop()
                    res = self._insertOne(item)
                    print('res=', res)
            else:
                raise Exception('插入数据库类型不正确（dict或list)', 'DB->insert')
            self._connect().commit()
        except BaseException as err:
            self._connect().rollback()
            traceback.print_exc()
            res = False
        self._initData()
        return res



    def first(self):
        self.sql = self._getBuilder().limit(1).operater('select').buildSql();
        self._getCursor().execute(self.sql)
        data = self._getCursor().fetchone()
        self._initData()
        return data

    def get(self):
        self.sql = self._getBuilder().operater('select').buildSql()
        self._getCursor().execute(self.sql)
        data = self._getCursor().fetchall()
        self._initData()
        return data

    def delete(self):
        try:
            self.sql = self._getBuilder().operater('delete').buildSql()
            res = self._getCursor().execute(self.sql)
            self._connect().commit()
        except:
            self._connect().rollback()
            traceback.print_exc()
        self._initData()
        return res
