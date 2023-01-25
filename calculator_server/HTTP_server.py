from http.server import HTTPServer
from calculator_server.daemon import CalcDaemon
from .daemon import Resources


HOST = ''
PORT = 8080


def main():
    try:

        _run_server()

    except KeyboardInterrupt:
        print("\rServer stopped manually.\n")


class HTTPServerWithResources(HTTPServer):

    def __init__(self, *args, **kwargs):
        http_server_resources = Resources()
        super().__init__(*args, **kwargs)


def _run_server(server_class=HTTPServerWithResources, handler_class=CalcDaemon):
    httpd = None

    try:

        server_address = (HOST, PORT)
        httpd = server_class(server_address, handler_class)
        print("\nServer started.")
        httpd.serve_forever()

    except Exception:
        if httpd is not None:
            httpd.server_close()
        raise


if __name__ == "__main__":
    main()
