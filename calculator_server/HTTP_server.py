from http.server import HTTPServer
from calculator_server.daemon import CalcDaemon


HOST = ''
PORT = 8080


def main():
    try:

        _run_server()

    except KeyboardInterrupt:
        print("\rServer stopped manually.\n")


def _run_server(server_class=HTTPServer, handler_class=CalcDaemon):
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
