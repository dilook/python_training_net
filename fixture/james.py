import telnetlib


class JamesHelper:
    def __init__(self, app):
        self.app = app

    def ensure_user_exists(self, username, password):
        pass

    class Session:

        def __init__(self, host, port, username, password):
            self.telnet = telnetlib.Telnet(host, port, 5)
            self.telnet.read_until("Login id:", 5)
            self.telnet.write(username + "\n")
            self.telnet.read_until("Password:", 5)
            self.telnet.write(password + "\n")
            self.telnet.read_until("Password:", 5)
