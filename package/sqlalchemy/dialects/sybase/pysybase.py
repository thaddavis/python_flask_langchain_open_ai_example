# sybase/pysybase.py
# Copyright (C) 2010-2023 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""
.. dialect:: sybase+pysybase
    :name: Python-Sybase
    :dbapi: Sybase
    :connectstring: sybase+pysybase://<username>:<password>@<dsn>/[database name]
    :url: https://python-sybase.sourceforge.net/

Unicode Support
---------------

The python-sybase driver does not appear to support non-ASCII strings of any
kind at this time.

"""  # noqa

from sqlalchemy import processors
from sqlalchemy import types as sqltypes
from sqlalchemy.dialects.sybase.base import SybaseDialect
from sqlalchemy.dialects.sybase.base import SybaseExecutionContext
from sqlalchemy.dialects.sybase.base import SybaseSQLCompiler


class _SybNumeric(sqltypes.Numeric):
    def result_processor(self, dialect, type_):
        if not self.asdecimal:
            return processors.to_float
        else:
            return sqltypes.Numeric.result_processor(self, dialect, type_)


class SybaseExecutionContext_pysybase(SybaseExecutionContext):
    def set_ddl_autocommit(self, dbapi_connection, value):
        if value:
            # call commit() on the Sybase connection directly,
            # to avoid any side effects of calling a Connection
            # transactional method inside of pre_exec()
            dbapi_connection.commit()

    def pre_exec(self):
        SybaseExecutionContext.pre_exec(self)

        for param in self.parameters:
            for key in list(param):
                param["@" + key] = param[key]
                del param[key]


class SybaseSQLCompiler_pysybase(SybaseSQLCompiler):
    def bindparam_string(self, name, **kw):
        return "@" + name


class SybaseDialect_pysybase(SybaseDialect):
    driver = "pysybase"
    execution_ctx_cls = SybaseExecutionContext_pysybase
    statement_compiler = SybaseSQLCompiler_pysybase

    supports_statement_cache = True

    colspecs = {sqltypes.Numeric: _SybNumeric, sqltypes.Float: sqltypes.Float}

    @classmethod
    def dbapi(cls):
        import Sybase

        return Sybase

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user", password="passwd")

        return ([opts.pop("host")], opts)

    def do_executemany(self, cursor, statement, parameters, context=None):
        # calling python-sybase executemany yields:
        # TypeError: string too long for buffer
        for param in parameters:
            cursor.execute(statement, param)

    def _get_server_version_info(self, connection):
        vers = connection.exec_driver_sql("select @@version_number").scalar()
        # i.e. 15500, 15000, 12500 == (15, 5, 0, 0), (15, 0, 0, 0),
        # (12, 5, 0, 0)
        return (vers / 1000, vers % 1000 / 100, vers % 100 / 10, vers % 10)

    def is_disconnect(self, e, connection, cursor):
        if isinstance(
            e, (self.dbapi.OperationalError, self.dbapi.ProgrammingError)
        ):
            msg = str(e)
            return (
                "Unable to complete network request to host" in msg
                or "Invalid connection state" in msg
                or "Invalid cursor state" in msg
            )
        else:
            return False


dialect = SybaseDialect_pysybase
