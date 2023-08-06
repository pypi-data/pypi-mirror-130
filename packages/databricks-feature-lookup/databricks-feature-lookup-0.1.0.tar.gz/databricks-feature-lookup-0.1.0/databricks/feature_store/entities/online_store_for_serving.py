from databricks.feature_store.entities.store_type import StoreType
from databricks.feature_store.entities.cloud import Cloud

from typing import Union


class MySqlConf:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class SqlServerConf:
    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port


class DynamoDbConf:
    def __init__(self, region: str):
        self._region = region

    @property
    def region(self):
        return self._region


class OnlineStoreForServing:
    def __init__(
        self,
        cloud: Cloud,
        store_type: StoreType,
        extra_config: Union[MySqlConf, SqlServerConf, DynamoDbConf],
        read_secret_prefix: str,
    ):
        self._cloud = cloud
        self._store_type = store_type
        self._extra_configs = extra_config
        self._read_secret_prefix = read_secret_prefix

    @property
    def cloud(self):
        return self._cloud

    @property
    def store_type(self):
        return self._store_type

    @property
    def extra_configs(self):
        return self._extra_configs

    @property
    def read_secret_prefix(self):
        return self._read_secret_prefix

    @property
    def password(self):
        return self._password

    @classmethod
    def from_proto(cls, the_proto):
        conf = None
        if the_proto.WhichOneof("extra_configs") == "mysql_conf":
            conf = MySqlConf(the_proto.mysql_conf.host, the_proto.mysql_conf.port)
        elif the_proto.WhichOneof("extra_configs") == "sql_server_conf":
            conf = SqlServerConf(
                the_proto.sql_server_conf.host, the_proto.sql_server_conf.port
            )
        elif the_proto.WhichOneof("extra_configs") == "dynamodb_conf":
            conf = DynamoDbConf(the_proto.dynamodb_conf.region)
        else:
            raise ValueError("Unsupported Store Type: " + str(the_proto))
        return cls(
            cloud=the_proto.cloud,
            store_type=the_proto.store_type,
            extra_config=conf,
            read_secret_prefix=the_proto.read_secret_prefix,
        )
