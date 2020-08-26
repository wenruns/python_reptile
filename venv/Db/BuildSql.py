
class BuildSql:
    # SQL生成器
    def __init__(self):
        self._conditions = {
            'or':[],
            'and':[],
        }
        self._orderBy = []
        self._groupBy = []
        self._limit = {}
        self._having = {
            'and':[],
            'or':[],
        }
        self._exist = []
        self._fields = []
        self._operate = 'select'
        self._sql = ''
        self._values = []
        self._tableName = ''
        self._alias = ''
        self._joins = []
        self._conditionValues = {}
        self.counter = 0

    def formatData(self, data):
        if not self._fields or self._fields is None:
            self._fields = ''
            self._values = ''
            for i in data:
                if self._operate == 'insert':
                    self._fields += i + ','
                    if isinstance(data[i], str):
                        self._values += '"%s",'
                    else:
                        self._values += '%s,'
                elif self._operate == 'update':
                    if isinstance(data[i], str):
                        self._values += i + '="%s",'
                    else:
                        self._values += i + '=%s,'
            self._fields = self._fields.strip(',')
            self._values = self._values.strip(',')
        return self;


    def table(self, tableName):
        self._tableName = tableName
        return self

    def alias(self, aliasName):
        self._alias = aliasName
        return self

    def join(self, tableName, primaryKey, operate = '=', foreignKey = '', type = 'left'):
        self._joins.append({
            'table':tableName,
            'operate': operate,
            'primaryKey':primaryKey,
            'foreignKey':foreignKey,
            'type':type,
        })
        return self

    # 添加
    def where(self, column, operate='', value=''):
        self._conditions['and'].append({
            'column': column,
            'operate': operate,
            'value': value,
        })
        return self

    def orWhere(self, column, operate = '', value = ''):
        self._conditions['or'].append({
            'column':column,
            'operate':operate,
            'value':value,
        })
        return self

    # having(subSql)
    def having(self, subSql, relation = 'and'):
        self._having[relation].append(subSql)
        return self

    # order by
    def orderBy(self, column, order='asc'):
        self._orderBy.append({
            'column': column,
            'order': order
        })
        return self

    # group by 字段
    def groupBy(self, column):
        self._groupBy.append(column)
        return self

    # limit限制
    def limit(self, length, offset=0):
        self._limit = {
            'length': length,
            'offset': offset,
        }
        return self

    def select(self, fields=[]):
        self._fields = fields
        return self

    def operater(self, operate='select'):
        self._operate = operate
        return self

    def buildSql(self):
        if self._operate == 'select':
            self._selectSql()
        elif self._operate == 'update':
            self._updateSql()
        elif self._operate == 'insert':
            self._insertSql()
        elif self._operate == 'delete':
            self._deleteSql()
        else:
            raise Exception('不存在操作：' + self._operate)
        return self._sql

    def makeSubSql(self):
        # print(self._conditions, self._tableName)
        if self._tableName:
            self.buildSql()
        else:
            sql = self._makeConditionStr()
            self._sql = sql.strip().strip('and').strip('or').strip('where').strip()
        return self._sql

    def _makeFieldStr(self):
        if isinstance(self._fields, str):
            return self._fields
        elif len(self._fields):
            fieldStr = ''
            for field in self._fields:
                fieldStr += field + ','
            return fieldStr.strip(',')
        else:
            return '*'

    def __condition(self, column, operate, value, relation, sqlStr):
        if not sqlStr or sqlStr is None:
            sqlStr += ' where '
        if (sqlStr != ' where '):
            sqlStr += ' ' + relation + ' '
        if hasattr(column, '__call__'):
            builder = BuildSql()
            column(builder)
            sqlStr += '(' + builder.makeSubSql() + ')'
            if value is not None:
                if isinstance(value, str):
                    sqlStr += ' ' + operate + ' "%s"'
                else:
                    sqlStr += ' ' + operate + ' %s'
                self._conditionValues['condition_closure'+self.counter] = value
                self.counter += 1
        else:
            if isinstance(value, str):
                sqlStr += column + ' ' + operate + ' "%s"'
            else:
                sqlStr += column + ' ' + operate + ' %s'
            self._conditionValues['condition_'+column] = value
        return sqlStr

    def getConditionValues(self):
        return self._conditionValues

    def _makeConditionStr(self):
        sqlStr = ''
        if len(self._conditions['and']):
            # self._conditions = self._conditions
            for (i,item) in enumerate(self._conditions['and']):
                sqlStr = self.__condition(item['column'], item['operate'], item['value'], 'and', sqlStr)

        if len(self._conditions['or']):
            for (i, item) in enumerate(self._conditions['or']):
                sqlStr = self.__condition(item['column'], item['operate'], item['value'], 'or', sqlStr)
        return sqlStr


    def _makeGroupByStr(self):
        groupStr = ''
        if len(self._groupBy):
            groupStr += ' group by '
            if isinstance(self._groupBy, str):
                groupStr += self._groupBy + ' '
            else:
                for field in self._groupBy:
                    groupStr += field + ','
            groupStr = groupStr.strip(',')
        return groupStr

    def __havingStr(self, subSql, relation, havingStr):
        if not havingStr or havingStr is None:
            havingStr += ' having '
        if havingStr != ' having ':
            havingStr += ' ' + relation + ' '
        if hasattr(subSql, '__call__'):
            builder = BuildSql()
            subSql(builder)
            subSql = builder.makeSubSql().strip()
        havingStr += subSql
        return havingStr


    def _makeHavingStr(self):
        havingStr = ''
        if len(self._having['and']):
            for item in self._having['and']:
                havingStr = self.__havingStr(item, 'and', havingStr)
        if len(self._having['or']):
            for item in self._having['or']:
                havingStr = self.__havingStr(item, 'or', havingStr)
        return havingStr

    def _makeOrderByStr(self):
        orderStr = ''
        if len(self._orderBy):
            orderStr += ' order by '
            for item in self._orderBy:
                orderStr += item['column'] + ' ' + item['order'] + ','
            orderStr = orderStr.strip(',')
        return orderStr

    def _makeLimitStr(self):
        if len(self._limit):
            return ' limit ' + str(self._limit['length']) + ' offset ' + str(self._limit['offset'])
        else:
            return ''

    def _makeAliasStr(self):
        if self._alias:
            return ' as ' + self._alias + ' '
        else:
            return ''

    def _makeJoinStr(self):
        joinStr = ''
        if len(self._joins):
            for item in self._joins:
                type = item['type']
                table = item['table']
                primaryKey = item['primaryKey']
                foreignKey = item['foreignKey']
                operate = item['operate']
                joinStr += type + ' join ' + table + ' on '
                if hasattr(primaryKey,'__call__'):
                    builder = BuildSql()
                    primaryKey(builder)
                    joinStr += builder.makeSubSql()
                else:
                    joinStr += primaryKey + operate + foreignKey
            joinStr += ' '
        return joinStr

    def _selectSql(self):
        self._sql = 'select ' + self._makeFieldStr() \
                    + ' from ' + self._tableName \
                    + self._makeAliasStr() \
                    + self._makeJoinStr() \
                    + self._makeConditionStr() \
                    + self._makeGroupByStr() \
                    + self._makeHavingStr() \
                    + self._makeOrderByStr()\
                    + self._makeLimitStr()

    def _updateSql(self):
        self._sql = 'update ' + self._tableName + ' set ' + self._values + self._makeConditionStr()

    def _insertSql(self):
        self._sql = 'insert into ' + self._tableName + ' (' + self._fields + ') values (' + self._values + ')'

    def _deleteSql(self):
        self._sql = 'delete from ' + self._tableName + self._makeConditionStr()
