from typing import Dict

from tabledbmapper.logger import Logger

from tabledbmapper.engine import TemplateEngine, QueryResult, CountResult, ExecResult
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.xml_config import parse_config_from_string, parse_config_from_file


class SQLSession:

    # session pool
    _session_pool = None

    # use index
    _index = -1

    # sql engine
    _engine = None

    # def __init__(self, template_engine: TemplateEngine, session_pool: SessionPool, index: int):
    def __init__(self, template_engine: TemplateEngine, session_pool=None, index=-1):
        """
        Init SQLSession
        :param session_pool: session_pool Convenient to close the session
        :param index: The database connection index being used
        :param template_engine: sql engine
        """
        self._engine = template_engine
        if session_pool is not None and index != -1:
            self._session_pool = session_pool
            self._index = index

            def commit():
                """
                Commit session
                """
                self._session_pool.commit_session(self._index)
            self.commit = commit

            def rollback():
                """
                Rollback session
                """
                self._session_pool.rollback_session(self._index)
            self.rollback = rollback

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._engine.destruction()
        self._engine = None
        if self._session_pool is not None:
            self._session_pool.give_back_session(self._index)
            self._session_pool = None
        self._index = -1

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._engine.set_logger(logger)
        return self

    def manager(self, config: dict) -> Manager:
        """
        Assemble upward as a manager
        :param config XmlConfig
        :return: manager
        """
        return Manager(self.engine(), config)

    def manager_by_string(self, config_string: str) -> Manager:
        """
        Assemble upward as a manager
        :param config_string xml string
        :return: manager
        """
        config = parse_config_from_string(config_string)
        return Manager(self.engine(), config)

    def manager_by_file(self, config_file: str) -> Manager:
        """
        Assemble upward as a manager
        :param config_file xml file
        :return: manager
        """
        config = parse_config_from_file(config_file)
        return Manager(self.engine(), config)

    def engine(self) -> TemplateEngine:
        """
        Assemble upward as a template engine
        :return: TemplateEngine
        """
        return self._engine

    def query(self, sql_template: str, parameter: Dict) -> QueryResult:
        return self._engine.query(sql_template, parameter)

    def count(self, sql_template: str, parameter: Dict) -> CountResult:
        return self._engine.count(sql_template, parameter)

    def exec(self, sql_template: str, parameter: Dict) -> ExecResult:
        return self._engine.exec(sql_template, parameter)
