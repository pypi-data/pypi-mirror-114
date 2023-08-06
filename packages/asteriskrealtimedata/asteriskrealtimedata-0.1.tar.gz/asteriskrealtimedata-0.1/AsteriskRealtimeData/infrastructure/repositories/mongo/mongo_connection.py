import os
import subprocess
from typing import Any
from antidote import service, inject
from AsteriskRealtimeData.environments import Config
from pymongo import MongoClient
from pymongo.database import Database
from asteriskinterfacelogger.logging import logger

from AsteriskRealtimeData.infrastructure.repositories.connection_interface import (
    Connection,
)


@service(singleton=True)
class MongoConnection(Connection):
    _database_connection: Any

    def __init__(self) -> None:
        super().__init__()
        self.connect(
            self.getHost(),
            self.getPort(),
            self.getUser(),
            self.getPassword(),
            self.getDatabase(),
        )

    def connect(
        self, host: str, port: int, user: str, password: str, database: str
    ) -> None:
        self._database_connection = Database(
            MongoClient(host=[host], document_class=dict, tz_aware=False, connect=True),
            database,
        )

    def get_connection(self) -> Any:
        return self._database_connection

    # client: MongoClient = None
    # database_connection: Database = None
    # mongodb_host: str
    # mongodb_port: str

    # def __init__(self) -> None:
    #     try:
    #         if self.database_connection is None:
    #             self.mongodb_host = self.get_mongodb_host()
    #             self.mongodb_port = self.get_mongodb_port()
    #             logger.info(
    #                 {
    #                     "action": "Connecting to MongoDb",
    #                     "host": self.mongodb_host,
    #                     "port": self.mongodb_port,
    #                 }
    #             )
    #             self.client = MongoClient(self.mongodb_host, self.mongodb_port)
    #             self.database_connection = self.client.asterisk
    #     except Exception as e:
    #         logger.error(
    #             {
    #                 "cause": "Can't connect mongodb",
    #                 "host": self.mongodb_host,
    #                 "port": self.mongodb_port,
    #                 "exception": e,
    #             }
    #         )

    # def get_connection(self):
    #     return self.database_connection

    # def get_mongodb_host(self):
    #     mongodb_host = os.environ.get("MONGODB_HOST", None)
    #     if mongodb_host is None:
    #         mongodb_host = self._search_mongodb_host_by_docker()
    #     return mongodb_host

    # def get_mongodb_port(self):
    #     mongodb_port = os.environ.get("MONGODB_PORT", 27017)
    #     return int(mongodb_port)

    # def _search_mongodb_host_by_docker(self):
    #     try:
    #         mongodb_host = subprocess.check_output(
    #             'docker inspect $(docker ps -q -f name=mongo) | grep -E "IPAddress.*[0-9]{1,3}" | grep -Eo "[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}"',
    #             stderr=subprocess.STDOUT,
    #             shell=True,
    #         )
    #         return str(mongodb_host.decode("utf-8")).replace("\n", "")
    #     except Exception as e:
    #         logger.error(
    #             {
    #                 "cause": "Error searching mongo host from docker",
    #                 "exception": e,
    #             }
    #         )
