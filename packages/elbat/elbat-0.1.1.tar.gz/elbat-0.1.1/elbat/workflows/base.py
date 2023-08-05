from abc import ABC, abstractmethod
from sqlalchemy import create_engine, Engine
from typing import Dict

# abstract workflow class. Must provide implementation
from loguru import logger


class Workflow(ABC):
    """Abstract class to handle running a workflow defined in a configuration"""

    workflow_type = "DEFAULT"

    def _init_(self, workflow_config, config):
        self._md = """
            # [{workflow_name}]


            ## Validation Status
            - batch id:
            - process queue id:
        """
        self._workflow_config = workflow_config
        self._workflow_name = workflow_config["name"]
        self._wf_object = {}
        self._db_engines: Dict[str, Engine]
        self._config = config
        self._messages = []
        self._is_db_engines_init: bool = False
        self._app_db_engine: bool = None
        self._is_smtp_init = False
        self._db_engines_loaded = False
        # self._workflow_id = workflow_id

        self.init()

    @property
    def db_engines(self):
        return self._db_engines

    @property
    def workflow_config(self):
        return self._workflow_config

    @property
    def config(self):
        return self._config

    @property
    def app_db_engine(self):
        return self._app_db_engine

    # @property
    # def workflow_type(self):
    #     return self.workflow_type

    @property
    def workflow_name(self):
        return self._workflow_name

    @abstractmethod
    def process(self):
        super()

    def init(self):

        # init databases
        if self._is_db_engines_init:
            logger.info("db engines already loaded.  skipping")
        else:
            try:

                self._db_engines = self._load_db_engines()
                # self._db_engines = self._get_db_connections()
                # self._get_db_connections()

                # logger.info('loading db engine configuration')
            except Exception as e:
                logger.info("unknown error occurred during db engine config.")
                logger.error("error loading db engines: {}".format(e))
                raise
            self._is_db_engines_init = True

        # set up app connections
        try:
            self._app_db_engine = self._db_engines["app"]
        except KeyError as e:
            logger.info(
                "unable to locate the application db engine.  validation config.yml."
            )
            logger.error("error loading app db engine: {}".format(e))
        except Exception as e:
            logger.info("unknown error occurred during application db engine.")
            logger.error("error loading app db engine: {}".format(e))
            raise

    def _load_db_engines(self):
        """Create a connection to the databases defined in your configurations"""
        config = self._config
        # logger.info('loading db engines')
        engines = {}
        for db in config["databases"].keys():
            if config["databases"][db]["rdbms"] == "oracle":
                engines.update(
                    {
                        db: create_engine(
                            "{dialect}://{username}:{password}@{service_name}".format(
                                dialect="oracle+cx_oracle",
                                username=config["databases"][db]["username"],
                                password=config["databases"][db]["password"],
                                service_name=config["databases"][db]["db_name"],
                            )
                        )
                    }
                )
            elif config["databases"][db]["rdbms"] == "mssql":

                engines.update(
                    {
                        db: create_engine(
                            "mssql+pyodbc://{user}:{password}@{dsn}".format(
                                dsn=config["databases"][db]["db_name"],
                                user=config["databases"][db]["username"],
                                password=config["databases"][db]["password"],
                            )
                        )
                    }
                )
            else:
                pass
        self._db_engines_loaded = True
        return engines
