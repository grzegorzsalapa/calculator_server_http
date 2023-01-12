import socket
from calculator_server import calculate, CalculationError

HOST = ''
PORT = 9010

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        try:
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
            print("\rServer off\n")
            break
