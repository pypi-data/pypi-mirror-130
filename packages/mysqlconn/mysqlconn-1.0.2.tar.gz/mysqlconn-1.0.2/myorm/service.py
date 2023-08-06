from typing import Dict

from superorm.dao import DAO
from superorm.engine import QueryResult, CountResult


class Service:
    """
    Basic service layer
    """
    _dao = None

    # Statement constants
    _get_list = "GetList"
    _get_count = "GetCount"
    _exist = "Exist"
    _get_model = "GetModel"
    _insert = "Insert"
    _update = "Update"
    _delete = "Delete"

    def __init__(self, dao: DAO):
        """
        Initialize service layer
        :param dao: Dao layer
        """
        self._dao = dao

    def get_list(self, parameter: Dict, **kwargs) -> QueryResult:
        """
        Get data list
        :param parameter: Search parameters
        :return: Data list
        """
        query_parameter = parameter.copy()
        # Compatible with previous writing
        if "Start" in query_parameter:
            query_parameter["mysql_mapper_limit_start"] = query_parameter["Start"]
        if "Length" in query_parameter:
            query_parameter["mysql_mapper_limit_length"] = query_parameter["Length"]
        # Processing parameters in kwargs
        if "order_by" in kwargs:
            query_parameter["mysql_mapper_order_by"] = kwargs["order_by"]
        if "start" in kwargs:
            query_parameter["mysql_mapper_limit_start"] = kwargs["start"]
        if "length" in kwargs:
            query_parameter["mysql_mapper_limit_length"] = kwargs["length"]
        return self._dao.query(self._get_list, query_parameter)

    def get_first(self, parameter: Dict, **kwargs) -> dict:
        """
        Get data list, then go back to the first record
        :param parameter: Search parameters
        :return: First Data
        """
        data_list = self.get_list(parameter, **kwargs)
        if len(data_list) == 0:
            return {}
        return data_list[0]

    def get_count(self, parameter: Dict) -> CountResult:
        """
        Quantity acquisition
        :param parameter: Search parameters
        :return: Number
        """
        return self._dao.count(self._get_count, parameter)

    def exist(self, parameter: Dict) -> bool:
        """
        Quantity acquisition, judge whether the quantity is greater than 0
        :param parameter: Search parameters
        :return: Number
        """
        query_parameter = parameter.copy()
        query_parameter["mysql_mapper_limit_start"] = 0
        query_parameter["mysql_mapper_limit_length"] = 1
        return self.get_count(parameter) > 1

    def get_model(self, parameter: Dict) -> Dict:
        """
        Get record entity
        :param parameter: Search parameters
        :return: Record entity
        """
        list_dict = self._dao.query(self._get_model, parameter)
        if len(list_dict) == 0:
            return {}
        return list_dict[0]

    def insert(self, parameter: Dict) -> int:
        """
        insert record
        :param parameter: insert data
        :return: Insert results
        """
        number, _ = self._dao.exec(self._insert, parameter)
        return number

    def update(self, parameter: Dict) -> int:
        """
        Update record
        :param parameter: Update data
        :return: Update results
        """
        _, number = self._dao.exec(self._update, parameter)
        return number

    def delete(self, parameter: Dict) -> int:
        """
        Delete data
        :param parameter: Delete data
        :return: Delete result
        """
        _, number = self._dao.exec(self._delete, parameter)
        return number
