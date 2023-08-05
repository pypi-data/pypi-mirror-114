from typing import Dict

class SimplePySQL:
    def  __init__(self, conditions: Dict={}, table: str="", columns: list or str="*", columns_values: Dict={}, operator: str="AND", clause: str="WHERE") -> None:
        self.conditions = conditions
        self.table = table
        print(self.table)
        if type(columns) == str:
            columns = [columns]
        self.columns = columns
        self.columns_values = columns_values
        self.operator = operator.upper()
        self.clause = clause.upper()

    def update(self):
        operator_conditions = f" {self.operator} ".join([f'"{column}"="{value}"' for column, value in self.conditions.items()])
        if_clause = "" if len(self.conditions) < 1 else self.clause
        dynamic_conditions = [if_clause, operator_conditions]
        columns_values = [f"{col} = '{val}'"for col, val in self.columns_values.items()]
        sql_statement = f"""UPDATE {self.table} SET {", ".join(columns_values)} {" ".join(dynamic_conditions)};"""
        return sql_statement

    def find(self):
        operator_conditions = f" {self.operator} ".join([f'"{column}"="{value}"' for column, value in self.conditions.items()])
        if_clause = "" if len(self.conditions) < 1 else self.clause
        dynamic_conditions = [if_clause, operator_conditions]
        sql_statement = f"""SELECT {", ".join(self.columns)} FROM {self.table} {" ".join(dynamic_conditions)};"""
        return sql_statement

    def insert(self):
        sql_statement = f"""INSERT INTO {self.table} ({", ".join([str(col) for col in self.columns_values.keys()])}) VALUES ({", ".join(["?" for _ in self.columns_values.values()])});"""
        return sql_statement
