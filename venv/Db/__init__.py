import MySQLdb
import MySQLdb.cursors
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
        self.doEscapeString = True


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
                cursorclass = MySQLdb.cursors.DictCursor,
            )

        return self.db

    # 获取游标
    def _getCursor(self):
        if not self.cursor or self.cursor is None:
            self.cursor = self._connect().cursor()
        return self.cursor

    # 执行sql
    def excute(self, sql = ''):
        if not sql or sql is None:
            if self.sql is None:
                print('over')
                return 0
            sql = self.sql
        res = self._getCursor().execute(sql)
        self._connect().commit()
        # res = self._getCursor().fetchall()
        if sql.find('select') == 0:
            res = self._getCursor().fetchall()
        elif sql.find('insert') == 0:
            res = self._getCursor().lastrowid
        return res

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

    def join(self, tableName, primaryKey, operate = '=', foreignKey = None, type='left'):
        self._getBuilder().join(tableName,primaryKey,operate, foreignKey, type)
        return self

    # 添加
    def where(self, column, operate = '', value = None):
        self._getBuilder().where(column, operate, value)
        return self

    def orWhere(self, column, operate = '', value = None):
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
        if not self.sql or self.sql is None:
            self.sql = self._getBuilder().operater('insert').formatData(data).buildSql()
        sql = self.sql % tuple(data.values())

        # print(sql)
        self._getCursor().execute(sql)
        return self._getCursor().lastrowid;

    # 插入数据
    def insert(self, data):
        try:
            if isinstance(data, dict):
                res = self._insertOne(data)
            elif isinstance(data, list):
                res = []
                while len(data):
                    item = data.pop()
                    res.append(self._insertOne(self.dictSort(item)))
            else:
                raise Exception('插入数据类型不正确（dict或list)', 'DB->insert')
            self._connect().commit()
        except BaseException as err:
            self._connect().rollback()
            traceback.print_exc()
            res = False
        self._initData()
        return res



    def first(self):
        self.sql = self._getBuilder().limit(1).operater('select').buildSql();
        self._getCursor().execute(self.sql % tuple(self._getBuilder().getConditionValues().values()))
        data = self._getCursor().fetchone()
        self._initData()
        return data

    def get(self):
        self.sql = self._getBuilder().operater('select').buildSql()
        self._getCursor().execute(self.sql % tuple(self._getBuilder().getConditionValues().values()))
        data = self._getCursor().fetchall()
        self._initData()
        return data

    def delete(self):
        try:
            self.sql = self._getBuilder().operater('delete').buildSql()
            res = self._getCursor().execute(self.sql % tuple(self._getBuilder().getConditionValues().values()))
            self._connect().commit()
        except:
            self._connect().rollback()
            traceback.print_exc()
            res = False
        self._initData()
        return res

    def _updateOne(self, item, where=[], orWhere=[]):
        conditionValues = self._getBuilder().getConditionValues()
        for field in where:
            value = item.pop(field)
            if(not self.sql or self.sql is None):
                self.where(field, '=', value)
            else:
                conditionValues['condition_'+field] = value
        for field in orWhere:
            value = item.pop(field)
            if(not self.sql or self.sql is None):
                self.orWhere(field, '=', value)
            else:
                conditionValues['condition_'+field] = value
        if not self.sql or self.sql is None:
            self.sql = self._getBuilder().operater('update').formatData(item).buildSql()
            print(self.sql)
        sql = self.sql % (*tuple(item.values()), *tuple(conditionValues.values()))
        print(sql)
        return self._getCursor().execute(sql)

    def update(self, data, where = [], orWhere=[]):
        try:
            if isinstance(data, dict):
                res = self._updateOne(data, where, orWhere)
            elif isinstance(data, list):
                res = 0
                while len(data):
                    item = data.pop()
                    res += self._updateOne(self.dictSort(item), where, orWhere)
            else:
                raise Exception('更新数据类型不正确（dict或list)', 'DB->update')
            self._connect().commit()
        except:
            self._connect().rollback()
            traceback.print_exc()
            return False
        return res
