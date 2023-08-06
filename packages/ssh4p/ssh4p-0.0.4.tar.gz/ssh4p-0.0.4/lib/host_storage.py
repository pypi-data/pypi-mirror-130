# encoding: UTF-8

from common import config_home, host_map_path
import json


class Host:
    def __init__(self, dict_data: dict):
        self.name = dict_data.get('name', None)
        self.host = dict_data.get('host', None)
        self.port = dict_data.get('host', None)
        self.user = dict_data.get('user', None)
        self.password = dict_data.get('password', None)
        self.proxy = dict_data.get('proxy', None)

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return str(self.to_dict())


class HostManager(object):

    @staticmethod
    def all() -> dict:
        with open(host_map_path) as file:
            host_map_json = json.load(file)

        host_map = dict()
        for key in host_map_json:
            host = Host(host_map_json[key])
            host.name = key
            host_map[key] = host
        return host_map

    @staticmethod
    def get(name: str) -> Host:
        return HostManager.all().get(name, None)


if __name__ == '__main__':
    HostManager.all()
