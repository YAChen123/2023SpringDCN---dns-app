from flask import Flask, request
import requests
import socket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello! This is User Server'

@app.route('/fibonacci')
def fibonacci():
    # Retreve the required parameters from GET HTTP request
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # check if parameters are missing
    if not hostname or not fs_port or not number or not as_ip or not as_port:
        return "Bad Request" , 400
    
    # Make a DNS query to the Authoritative Server to get the IP address of the Fibonacci Server
    dns_query = f"TYPE=A\nNAME={hostname}"

    # Send the request message to AS via UDP on port 53533
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(dns_query.encode(), (as_ip, int(as_port)))

    # receive the response from the AS
    response, address = sock.recvfrom(1024)
    dns_response = response.decode().split("\n")
    
    # Parse the DNS response to get the IP address of the Fibonacci Server
    if len(dns_response) == 0 or dns_response[0] != "TYPE=A":
        return "DNS query failed", 500
    ip_address = dns_response[2].split("=")[1]

    # Make a request to Fibonacci Server to get Fibonacci Number
    fibonacci_query = f"http://{ip_address}:{fs_port}/fibonacci?number={number}"
    response = requests.get(fibonacci_query, )

    # Return the Fibonacci Number or an error if request failed
    if(response.status_code != 200):
        return "Fibonacci request failed", 500
    
    return response.text, 200

app.run(host='0.0.0.0',
        port=8080,
        debug=True)

