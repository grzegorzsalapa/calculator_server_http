import socket
from .calculate import calculate, CalculationError


def main():
    HOST = ''
    PORT = 9010

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            print('\nServer started.')
            while True:
                s.listen(1)
                conn, addr = s.accept()
                with conn:
                    print('\nConnected by ', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        expression = str(data)[2:][:-1]
                        print('Received expression: ', expression)
                        try:
                            result = str(calculate(expression))
                        except CalculationError as e:
                            result = str(e)
                        print('Returned result: ', result)
                        data = bytes(result, 'utf-8')
                        conn.sendall(data)

    except KeyboardInterrupt:
        print("\rServer stopped.\n")


if __name__ == "__main__":
    main()
