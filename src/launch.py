import json

from webserver import Webserver

with open('configs/config.json') as config_file:
    playlist = json.load(config_file)["playlist"]

if __name__ == '__main__':
    webserver = Webserver(playlist)
    webserver.run()