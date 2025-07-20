#!/usr/bin/env python3
"""backend module for the roaming plans SQLite database
"""

# constants ----------------------------------------------------------------------------------
import json
import pandas as pd
import sqlite3
from base import BaseHandler


# constants ----------------------------------------------------------------------------------
DB_PATH = 'plans.sqlite'
DB_SCHEMA_PATH = 'data/schema.json'


# helper functions -------------------------------------------------------------------------------------
def create_table_sql(table_name: str, columns: list[dict]) -> str:
    col_defs = []
    for col in columns:
        name = col['column_name']
        dtype = col['data_type']
        nullable = "" if col.get('nullable', 0) == 1 else "NOT NULL"
        primary = "PRIMARY KEY AUTOINCREMENT" if col.get('primary_key', 0) == 1 else ""
        
        parts = [name, dtype, primary, nullable]
        col_def = " ".join(part for part in parts if part).strip()
        col_defs.append(col_def)

    col_clause = ",\n    ".join(col_defs)
    create_stm = f"CREATE TABLE {table_name} (\n    {col_clause}\n);"
    return create_stm


# classes ---------------------------------------------------------------------------------------------------------
class DBConnector(BaseHandler):
    def __init__(self, db_path='', schema_file='', schema=[]):
        self.db_path: str = db_path or DB_PATH
        self.schema_file: str = schema_file or DB_SCHEMA_PATH
        self.schema: list[dict] = schema
        self.conn = None
        self.cursor = None
        super().__init__()
        self._set_schema()

    def _set_schema(self):
        if not self.schema:
            with open(self.schema_file) as f:
                self.schema = json.load(f)
                f.close()

        self.tables = self.schema.copy()
        self.table_names = [t['table_name'] for t in self.tables]

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.status()}]>'

    def connected(self):
        return self._status_code == 1

    def commit(self, is_fatal=True, re_raise=False):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            self._exception_handle(exception=e, is_fatal=is_fatal, re_raise=re_raise)
            return False

    def execute(self, stm, args=None, is_fatal=False, re_raise=False):
        try:
            if args:
                self.cursor.execute(stm, args)
            else:
                self.cursor.execute(stm)
            return True
        except Exception as e:
            self._exception_handle(exception=e, is_fatal=is_fatal, re_raise=re_raise)
            return False

    def build(self, keep_open=False):
        connect_success = self.connect()
        if connect_success:
            try:
                self.tables_drop()
                self.tables_create()
                self.data_insert()
                self.commit()
                if not keep_open:
                    self.close()
            except Exception as e:
                msg = 'build failed'
                self._exception_handle(msg=msg, exception=e)
                return False
            else:
                if self._status_code == 1:
                    return True
                else:
                    return False
        else:
            return False

    def data_insert(self):
        for table in self.tables:
            table_name = table['table_name']
            filepath = table['filepath']
            try:
                df = pd.read_csv(filepath)
                df.to_sql(table_name, self.conn, if_exists="append", index=False)
            except Exception as e:
                msg = f'failed to insert data for table {table_name}'
                self._exception_handle(msg=msg, exception=e, re_raise=True)

    def tables_drop(self):
        for t in self.table_names:
            self.table_drop(t)

    def table_drop(self, table_name):
        SQL_DROP = f'DROP TABLE IF EXISTS {table_name};'
        self.execute(SQL_DROP, re_raise=True)

    def tables_create(self):
        for t in self.table_names:
            self.table_create(t)

    def table_create(self, table_name):
        table_config = [t for t in self.tables if t['table_name']==table_name][0]
        columns = table_config.get('columns', [])
        create_tbl_stm = create_table_sql(table_name, columns)
        self.execute(create_tbl_stm, re_raise=True)

    def connect(self):
        if not self.connected():
            try:
                self.conn = sqlite3.connect(DB_PATH)
                self.cursor = self.conn.cursor()
                self._status_code = 1
                return True
            except Exception as e:
                msg = 'problem connecting to database'
                self._exception_handle(msg=msg, exception=e)
                return False
        else:
            return True

    def exit(self):
        self.close()
        if self.conn:
            self.conn = None
            self.cursor = None

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                return True
            except Exception as e:
                msg = 'problem closing db connection'
                self._exception_handle(msg=msg, exception=e, is_fatal=False)
                return False

# entry point ----------------------------------------------------------------------------------------
def db_build():
    db = DBConnector()
    success = db.build()
    errors = db.error
    return success, errors


if __name__ == '__main__':
    db_build()