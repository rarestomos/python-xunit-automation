import configparser

from configuration import ENV_NAME


class TestConfiguration:

    def __init__(self):
        self.configuration = configparser.ConfigParser(allow_no_value=True)
        self.configuration.read("test_configuration.ini")
        self.backend_url = self.configuration[ENV_NAME]["backend_url"]

    def read_configuration(self):
        self.books_url = f'{self.backend_url}/books'
        self.users_url = f'{self.backend_url}/users'
        self.reservations_url = f'{self.backend_url}/reservations'
