from flask import Flask, request
import socket
import json

app = Flask(__name__)

hostname = None
ip = None
as_ip = None
as_port = None

@app.route('/')
def hello_world():
    return 'Hello! This is Fibonacci Server'

@app.route('/register', methods=['PUT'])
def register():
    global hostname, ip, as_ip, as_port
    data = json.loads(request.data.decode())
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    # Registration to Authoritative Server
    udp_msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"

    # Send the registration message to AS via UDP on port 53533
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(udp_msg.encode(), (as_ip, int(as_port)))

    # receive the response from the AS
    response, address = sock.recvfrom(1024)
    response_data = response.decode()
    print(f"Response from AS: {response_data}")

    # close the socket
    sock.close()
    return 'Fibonacci server registered with the Authoritative Server!', 201


@app.route('/fibonacci')
def fibonacci():
    print("got request from US")
    try:
        n = int(request.args.get('number'))
    except ValueError:
        return 'Bad Request - Number must be an integer', 400
    if n <= 0:
        return 'Bad Request - Number must be a positive integer', 400
    
    # Calculate Fibonacci Number
    fib_number = fibonacci_number(n)
    print(fib_number)
    return str(fib_number), 200


def fibonacci_number(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_number(n-1) + fibonacci_number(n-2)


app.run(host='0.0.0.0',
        port=9090,
        debug=True)
