from myorm.mapper import get_mapper_xml
from myorm.service import Service
from superorm.dao import DAO
from superorm.logger import Logger
from superorm.factory import SQLSessionFactory, SQLSessionFactoryBuild
from superorm.manager import Manager
from superorm.mapper import parse4string

from myorm.engine import MySQLConnHandle, MySQLExecuteEngine, MySQLConnBuilder
from myorm.info import table_xml, column_xml, index_xml, key_xml, get_db_info, get_table_info


class MySQLSessionFactory(SQLSessionFactory):

    # Database conn info
    _conn_builder = None

    # Database description information
    database_info = None

    # Database table info
    table_info = None

    # Service dictionary
    _services = None

    def __init__(self, conn_builder: MySQLConnBuilder, conn_handle: MySQLConnHandle, execute_engine: MySQLExecuteEngine,
                 lazy_init: bool, max_conn_number: int, logger: Logger):
        """
        Init session pool
        :param conn_builder: MySQLConnBuilder
        :param conn_handle: MySQLConnHandle
        :param execute_engine: MySQLExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param logger: Logger
        """
        super().__init__(conn_builder, conn_handle, execute_engine, lazy_init, max_conn_number, logger)
        self._conn_builder = conn_builder
        self.load_dao("orm_table_info_dao", parse4string(table_xml))
        self.load_dao("orm_column_info_dao", parse4string(column_xml))
        self.load_dao("orm_index_info_dao", parse4string(index_xml))
        self.load_dao("orm_key_info_dao", parse4string(key_xml))
        self.database_info = {}
        self.table_info = {}
        self._services = {}

    def get_service(self, service_name: str) -> Service:
        """
        Get service
        :param service_name: service name
        :return: DAO
        """
        return self._services[service_name]

    def load_service(self):
        """
        load database service
        :return: self
        """
        _db_info = get_db_info(self._dao, self._conn_builder.database)
        return self._load_service(_db_info)

    def load_service_by_table_name(self, table_name: str):
        """
        used by load table,s service when close the simple service
        :param table_name: database table name
        :return: self
        """
        _db_info = get_table_info(self._dao, self._conn_builder.database, table_name)
        return self._load_service(_db_info)

    def _load_service(self, database_info: dict):
        """
        load service from database info
        :param database_info: database info
        :return: self
        """
        # for item table in database info
        for table in database_info["tables"]:
            # get mapper xml
            xml_string = get_mapper_xml(database_info, table["Name"])
            # parse to config
            config = parse4string(xml_string)
            # get manager
            manager = Manager(self._engine, config, self._logger)
            # get dao
            dao = DAO(self._session_manager, manager)

            # get the database info && set the table info
            self.table_info[table["Name"]] = table
            # get service
            self._services[table["Name"]] = Service(dao)
        # update the database info
        self.database_info["tables"] = list(self.table_info.values())
        return self


class MySQLSessionFactoryBuild(SQLSessionFactoryBuild):

    def __init__(self, host: str, user: str, password: str, database: str, port=3306, charset="utf8"):
        """
        Init
        :param host: host
        :param user: user
        :param password: password
        :param database: database
        :param port: data source port
        :param charset: charset
        """
        conn_builder = MySQLConnBuilder(host, user, password, database, port, charset)
        super().__init__(conn_builder, MySQLConnHandle(), MySQLExecuteEngine())

    def build(self) -> MySQLSessionFactory:
        return MySQLSessionFactory(
            self._conn_builder,
            self._conn_handle,
            self._execute_engine,
            self._lazy_init,
            self._max_conn_number,
            self._logger
        )
