import configparser

from configuration import ENV_NAME


class DevConfiguration:

    def __init__(self):
        self.configuration = configparser.ConfigParser(allow_no_value=True)
        self.configuration.read("dev_configuration.ini")
        self.backend_url = self.configuration[ENV_NAME]["backend_url"]

    def read_configuration(self):
        pass
