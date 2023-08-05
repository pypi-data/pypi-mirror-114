from paramiko import SSHClient, AutoAddPolicy


class Client(SSHClient):
    def __init__(self):
        super().__init__()
        self.set_missing_host_key_policy(AutoAddPolicy())
