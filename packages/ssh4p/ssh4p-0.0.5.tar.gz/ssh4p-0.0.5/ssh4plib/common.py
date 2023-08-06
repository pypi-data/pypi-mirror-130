# encoding: utf-8
import os

config_dir = '.ssh4p'
config_home = os.path.join(os.path.expanduser('~'), config_dir)
host_map_file = 'host_map.json'
host_map_path = os.path.join(config_home, host_map_file)
