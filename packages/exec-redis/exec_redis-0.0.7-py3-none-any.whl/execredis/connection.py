from abc import ABC
from redis import ConnectionPool, StrictRedis
from rediscluster import ClusterConnectionPool, RedisCluster


class ClientsConnection(StrictRedis):
    def __init__(self, **kwargs):
        super(ClientsConnection, self).__init__(**{**dict(
            connection_pool=ConnectionPool(host=kwargs.pop('host', 'localhost'), db=kwargs.pop('db', 0), **kwargs),
            decode_responses=True)}
        )


class ClusterClientsConnection(RedisCluster, ABC):
    def __init__(self, **kwargs):
        super(ClusterClientsConnection, self).__init__(**{**dict(
            connection_pool=ClusterConnectionPool(
                host=kwargs.pop('host', 'localhost'), db=kwargs.pop('db', 0), **kwargs),
            decode_responses=True)}
        )
