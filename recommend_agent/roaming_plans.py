#!/usr/bin/env python3
"""backend module for the roaming plans SQLite database
"""

# constants ----------------------------------------------------------------------------------
import pandas as pd
import sqlite3


# constants ----------------------------------------------------------------------------------
DB_PATH = 'plans.sqlite'
CSV_FILES = [
    {
        'table_name': 'plan',
        'filepath': 'data/roaming_plan.csv',
        'columns': [
            {
                'column_name': 'id',
                'data_type': 'INTEGER',
                'primary_key': 1,
                'nullable': 0
            },
            {
                'column_name': 'zone',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 0
            },
            {
                'column_name': 'duration_days',
                'data_type': 'INTEGER',
                'primary_key': 0,
                'nullable': 0
            },
            {
                'column_name': 'data_gb',
                'data_type': 'REAL',
                'primary_key': 0,
                'nullable': 0
            },
            {
                'column_name': 'price_sgd',
                'data_type': 'REAL',
                'primary_key': 0,
                'nullable': 0
            }
        ]
    },
    {
        'table_name': 'ppu_rate',
        'filepath': 'data/ppu_rate.csv',
        'columns': [
            {
                'column_name': 'zone',
                'data_type': 'INTEGER',
                'primary_key': 1,
                'nullable': 0
            },
            {
                'column_name': 'data_rate',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 1
            },
            {
                'column_name': 'call_outgoing',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 1
            },
            {
                'column_name': 'call_incoming',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 1
            },
            {
                'column_name': 'sms_rate',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 1
            }
        ]
    },
    {
        'table_name': 'destination',
        'filepath': 'data/destinations.csv',
        'columns': [
            {
                'column_name': 'id',
                'data_type': 'INTEGER',
                'primary_key': 1,
                'nullable': 0
            },
            {
                'column_name': 'country',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 0
            },
            {
                'column_name': 'zone',
                'data_type': 'TEXT',
                'primary_key': 0,
                'nullable': 0
            }
        ]
    }
]


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
class DBConnector():
    def __init__(self, db_path='', csv_files=[]):
        self.db_path: str = db_path or DB_PATH
        self.csv_files: list[dict] = csv_files or CSV_FILES
        self.tables = self.csv_files.copy()
        self.table_names = [t['table_name'] for t in self.tables]
        self.conn = None
        self.cursor = None
        self._status_code: int = 0
        self.error: str = ''

    def __repr__(self):
        return f'<{__class__} [{self.status}]>'

    def status(self):
        if self._status_code == 0:
            return 'READY'
        elif self._status_code == 1:
            return 'CONNECTED'
        else:
            return 'ERROR'

    def _exception_handle(self, msg='', exception=None, is_fatal=True, re_raise=False):
        ex_msg = f'ERROR. {msg} {exception}'
        self.error = ex_msg

        if is_fatal:
            self._status_code = 2
            self.close()

        if re_raise and exception:
            raise RuntimeError(ex_msg) from exception

    def connected(self):
        return self._status_code == 1

    def commit(self, is_fatal=True, re_raise=False):
        try:
            self.conn.commit()
            return True
        except Exception as e:
            self._exception_handle(exception=e, is_fatal=is_fatal, re_raise=re_raise)
            return False

    def execute(self, stm, is_fatal=True, re_raise=False):
        try:
            self.cursor.execute(stm)
            return True
        except Exception as e:
            self._exception_handle(exception=e, is_fatal=is_fatal, re_raise=re_raise)
            return False

    def build(self):
        connect_success = self.connect()
        if connect_success:
            self.tables_drop()
            self.tables_create()
            self.data_insert()
            self.commit()
            self.close()
            return True

    def data_insert(self):
        for table in self.tables:
            table_name = table['table_name']
            filepath = table['filepath']
            try:
                df = pd.read_csv(filepath)
                df.to_sql(table_name, self.conn, if_exists="append", index=False)
            except Exception as e:
                msg = f'failed to insert data for table {table_name}'
                self._exception_handle(msg=msg,exception=e)
                break

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
        if not self.cursor:
            try:
                self.conn = sqlite3.connect(DB_PATH)
                self.cursor = self.conn.cursor()
                self._status_code = 1
                return True
            except Exception as e:
                msg = 'problem connecting to database'
                self._exception_handle(msg=msg, exception=e)
                return False

    def close(self):
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
                self.cursor = None
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