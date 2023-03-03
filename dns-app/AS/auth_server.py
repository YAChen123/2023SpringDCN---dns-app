import socket
import os

# Define the port number and the IP address to listen on
UDP_PORT = 53533
IP_ADDRESS = '0.0.0.0'

# Define the file to store the DNS records
DNS_FILE = 'dns_records.txt'

# Create a UDP socket and bind it to the specified IP address and port number
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((IP_ADDRESS, UDP_PORT))

# Check if the dns_records file exists, create it if it does not
if not os.path.exists(DNS_FILE):
    with open(DNS_FILE, 'w') as f:
        f.write('')

# Define a dictionary to store the DNS records
dns_records = {}

# Read the DNS records from the file and populate the dictionary
with open(DNS_FILE, 'r') as f:
    for line in f:
        fields = line.strip().split(',')
        record_type = fields[0]
        hostname = fields[1]
        ip_address = fields[2]
        ttl = fields[3]
        dns_records[hostname] = (record_type, ip_address, ttl)

# Start listening for incoming UDP packets
while True:
    # Receive a UDP packet
    data, addr = sock.recvfrom(1024)

    # Decode the packet data as a string
    packet = data.decode()

    # Parse the packet fields (assuming the format is: "TYPE=A\nNAME=hostname\nVALUE=ip_address\nTTL=ttl")
    fields = packet.split("\n")

    # Handle DNS Query
    if len(fields) == 2 and fields[0] == "TYPE=A":
        print(f"Handle DNS record: {packet}")
        record_type = fields[0].split('=')[1]
        hostname = fields[1].split('=')[1]
        ip_address = dns_records.get(hostname)[1]
        ttl = dns_records.get(hostname)[2]

        # Construct a DNS response packet
        response_packet = f"TYPE={record_type}\nNAME={hostname}\nVALUE={ip_address}\nTTL={ttl}".encode()

        # Send the DNS response packet back to the client
        sock.sendto(response_packet, addr)
        
    # Handle Register
    else:
        record_type = fields[0].split('=')[1]
        hostname = fields[1].split('=')[1]
        ip_address = fields[2].split('=')[1]
        ttl = fields[3].split('=')[1]

         # Register the DNS record in the dictionary
        dns_records[hostname] = (record_type, ip_address, ttl)

        # Write the updated DNS records to the file
        with open(DNS_FILE, 'w') as f:
            for hostname, (record_type, ip_address, ttl) in dns_records.items():
                f.write(f"{record_type},{hostname},{ip_address},{ttl}\n")

        # Print a message to indicate the DNS record has been registered
        print(f"Registered DNS record: {hostname} -> {ip_address}")

        # Construct a DNS response packet
        response_packet = f"TYPE={record_type}\nNAME={hostname}\nVALUE={ip_address}\nTTL={ttl}".encode()

        print(dns_records)

        # Send the DNS response packet back to the client
        sock.sendto(response_packet, addr)
