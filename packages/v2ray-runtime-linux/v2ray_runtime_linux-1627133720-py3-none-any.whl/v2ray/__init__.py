import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = BASE_DIR.replace('\\', '/')

V2RAY_RUNTIME_DIR = BASE_DIR + '/v2ray_runtime'
CADDY_RUNTIME_NAME = 'v2ray'
CADDY_RUNTIME_PATH = V2RAY_RUNTIME_DIR + '/' + CADDY_RUNTIME_NAME
