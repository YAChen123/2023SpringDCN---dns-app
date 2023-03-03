# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install the required packages
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the required files to the container
COPY auth_server.py .

EXPOSE 53533/udp

# Start the servers
CMD ["python", "auth_server.py"]