from execredis.connection import ClientsConnection, ClusterClientsConnection


class ExecRedisClients:
    def __new__(cls, clients_name, redis_config=None):
        cls.__redis_config = (redis_config or {}).get(clients_name, {})
        cls.__cluster = cls.__redis_config.get('cluster', None)
        cls.__client_config = {k: v for k, v in cls.__redis_config.items() if k != 'cluster'}
        if cls.__cluster:
            return ClusterClientsConnection(**cls.__client_config)
        else:
            return ClientsConnection(**cls.__client_config)
