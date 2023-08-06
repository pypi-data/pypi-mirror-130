# encoding: UTF-8
import json

from ssh4plib.host_storage import Host, HostStorage


class Manager(object):

    @staticmethod
    def list():
        host_list = HostStorage.all().values()
        Manager.__print_header_line__()
        for host in host_list:
            Manager.__print_line__(host)

    @staticmethod
    def __print_header_line__():
        Manager.__print_line__(Host(name="NAME", host="HOST", port="PORT", user="USER", password="PASSWORD", proxy="PROXY"))

    @staticmethod
    def __print_line__(host: Host):
        size = 20
        print(str(host.name).ljust(size) + str(host.host).ljust(size) + str(host.port).ljust(10) + str(host.user).ljust(
            10) + str(host.password).ljust(30) + str(host.proxy).ljust(size))
