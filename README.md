# 2023 Spring DCN 
## Lab 3: Develop Simplified Authoritative Server for a Network of Applications

### Overview
![Lab steps](lab-instruction/auth-servers-interaction.jpeg)

### Setup
1. Open your terminal and clone the repository
`git clone ...`

2. Inside the folder, run the command
`docker-compose up -d`

3. Now the docker has run three servers, User Server, Fibonacci Server, and Authoritative Server.
There is a docker network called **DCN_lab3** that communiate the server to each other. <br> 
You can get User Server, Fibonacci Server, and Authoritative Server ip_address by typing `docker inspect DCN_lab3`

4. Open Postman and Register Fibonacci Server to Authoritative Server by running put api `http://localhost:9090/register` with body `{
    "hostname" : "fibonacci.com",
    "ip" : "fibonacci-server-ip-from-DCN_lab3",
    "as_ip" : "auth-server-ip-from-DCN_lab3",
    "as_port" : "53533"
}`  in your web browser. Now we have register the fibonacci.com ip-address to the Authoritative Server

5. User visit `http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=10&as_ip=auth-server-ip-from-DCN_lab3&as_port=53533`


