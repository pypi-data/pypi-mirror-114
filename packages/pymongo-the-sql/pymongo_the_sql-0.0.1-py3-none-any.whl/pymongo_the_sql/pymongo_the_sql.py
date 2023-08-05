from .simple_py_sql import SimplePySQL
import sqlite3
import os
from copy import deepcopy

class PyMongoTheSql:
    mongo_methods = {}
    def __init__(self, db_directory: str="./", db_uri: str=None):
        self.db_directory = db_directory
        self.db_uri = db_uri
        self.table = None

    def get_database(self, db_name: str):
        con = PyMongoTheSql
        self.name = db_name
        self.path = os.path.join(self.db_directory, f"{self.name}.sqlite3")
        self.database_uri = f"{self.path}"
        con.db = sqlite3.connect(self.database_uri)
        con.db.row_factory = sqlite3.Row
        con.db_cursor = con.db.cursor()
        get_tables_sql = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = con.db_cursor.execute(get_tables_sql).fetchall()
        for table in tables:
            key = "".join(table)
            self.table = key
            this = deepcopy(self)
            this.mongo_methods[key] = this
        return this.mongo_methods

    def run_db_cmd(self, sql_statement: str="", values: tuple = ()):
        db = PyMongoTheSql.db
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(sql_statement, values)
        db.commit()
        try:
            rows = cursor.fetchall()
            result = []
            for row in rows:
                data = {}
                keys = row.keys()
                for key in keys:
                    data[key] = row[key]
                result.append(data)
            return result[0] if len(result) == 1 else result
                
        except Exception:
            return True

    def update_all(self, columns_values):
        sql = SimplePySQL(table=self.table, columns_values=columns_values)
        sql_statement = sql.update()
        return self.run_db_cmd(sql_statement)

    def find_all(self):
        sql = SimplePySQL(table=self.table)
        sql_statement = sql.find()
        return self.run_db_cmd(sql_statement)

    def update(self, columns_values, conditions={}, operator=""):
        sql = SimplePySQL(table=self.table, columns_values=columns_values, conditions=conditions, operator=operator)
        sql_statement = sql.update()
        return self.run_db_cmd(sql_statement)

    def update_blob(self, columns_values, values=(), conditions={}, operator=""):
        sql = SimplePySQL(table=self.table, columns_values=columns_values, conditions=conditions, operator=operator)
        sql_statement = sql.update()
        return self.run_db_cmd(sql_statement.replace("'", ""), values)
    
    def find(self, conditions, columns=["*"], operator=""):
        sql = SimplePySQL(table=self.table, conditions=conditions, columns=columns, operator=operator)
        sql_statement = sql.find()
        return self.run_db_cmd(sql_statement)
    
    def insert(self, columns_values):
        sql = SimplePySQL(table=self.table, columns_values=columns_values)
        sql_statement = sql.insert()
        values = tuple(columns_values.values())
        return self.run_db_cmd(sql_statement, values)

    def find_one(self, conditions={}, columns=["*"], operator=""):
        result = self.find(conditions, columns=columns, operator=operator)
        if (type(result) == list and len(result) > 0):
            return result[0]
        return None

    def find_last(self, conditions={}, columns=["*"], operator=""):
        return (self.find(conditions, columns=columns, operator=operator))[-1]

    def update_one(self, columns_values, conditions={}):
        _id =  self.find_one(["id"], conditions)
        return self.update(columns_values, {"id": _id})
    
    def find_all_and_count(self):
        result =  self.find_all()
        return len(result)

    def find_and_count(self, conditions={}, columns=["*"], operator=""):
        result =  self.find(conditions, columns=columns, operator=operator)
        return len(result)
