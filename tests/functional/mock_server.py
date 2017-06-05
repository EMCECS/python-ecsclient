import os

from wsgiref.simple_server import make_server
from mock_server.application import Application


if __name__ == "__main__":
    mock_app = Application(7777, "localhost",
                           os.path.join(os.path.dirname(__file__), "api/"),
                           False, "application.json")
    httpd = make_server("", 8089, mock_app).serve_forever()
