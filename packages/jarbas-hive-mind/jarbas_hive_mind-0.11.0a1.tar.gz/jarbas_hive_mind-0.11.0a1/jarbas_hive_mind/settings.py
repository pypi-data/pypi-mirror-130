import xdg.BaseDirectory

DATA_PATH = xdg.BaseDirectory.save_data_path("jarbasHiveMind")

DEFAULT_PORT = 5678
USE_SSL = True

LOG_BLACKLIST = []

MYCROFT_WEBSOCKET_CONFIG = {
    "host": "0.0.0.0",
    "port": 8181,
    "route": "/core",
    "ssl": False
}
