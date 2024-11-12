from sqlmodel import text
from ..abstract_builder import AbstractBuilder

"""
过滤器
"""


class HasFilter(AbstractBuilder):
    __condition_builders = {
        'AND': 'build_and_condition',
        'OR': 'build_or_condition',
    }

    def __init__(self, connect):
        super().__init__(connect)
        self.wheres = None

    def build_not_condition(self,operator,condition):
        pass
    def build_and_condition(self,operator,condition):
        parts = []
        for operand in condition:
            if type(operand) in [list,dict]:
                operand=self.build_where(operand)
            if type(operand)==str:
                parts.append(operand)
        return '('+f' {operator} '.join(parts)+')';


    """
    通用条件过滤
    """

    def where(self, column, operator=None, value=None, boolean: str = 'and'):
        if callable(column):
            query = column(self.new_query())
            self.where(query.wheres)
        else:
            filter = [boolean, [operator, column, value]] if type(column) == str else column
            if self.wheres is None:
                self.wheres = filter
            else:
                self.wheres = [boolean, self.wheres, filter]
        return self

    """
    剔除为空的条件过滤
    """

    def filter_where(self, condition: dict, boolean: str = 'and'):
        if type(column) == dict:
            for k, v in column.items():
                self.filter_where(k, '==', v)
        elif value != '':
            self.where(column, operator, value)
        return self

    """
    in查询
    """

    def where_in(self, column, value: list, boolean: str = 'and', is_not: bool = False):
        operator = 'in' if is_not is False else 'not in'
        return self.where(column, operator, value, boolean)

    def where_raw(self, value: str, boolean: str = 'and'):
        if self.wheres is None:
            self.wheres = value
        else:
            self.wheres = [boolean, self.wheres, value]
        return self

    def build_simple_condition(self,operator,condition):
        if type(condition)!=list or len(condition)!=2:
            raise Exception(f"Operator {operator} requires two operands.")
        column=condition[0]
        value=condition[1]
        return f"{column} {operator} {value}"

    def build_where(self,condition):
        if type(condition)==str:
            return condition
        if type(condition)==dict:
            return self.build_hash_condition(condition)
        operator=condition[0]
        method=self.__condition_builders[str(condition[0]).upper()]  if str(condition[0]).upper() in self.__condition_builders else 'build_simple_condition'
        condition.pop(0)
        return getattr(self,method)(operator,condition)

    def build_in_condition(self,operator,condition):
        sql_values=[]
        if type(condition)==list and len(condition)==2 and type(condition[1])==list:
            string_value =','.join(str(arg) for arg in condition[1])
            return f"{condition[0]} in ({string_value})"
        return '0=1'

    """
    处理对象
    """
    def build_hash_condition(self,condition:dict):
        parts=[]
        for column,value in condition.items():
            if type(value)==list:
                parts.append(self.build_in_condition('IN',[column,value]))
            else:
                if value is None:
                    parts.append(f'{column} is NULL')
                else:
                    parts.append(f'{column}="{value}"')
        return parts[0] if len(parts)==1 else ' and '.join(parts)


    def filter(self, query):
        return query if self.wheres is None else query.where(text(self.build_where(self.wheres)))
