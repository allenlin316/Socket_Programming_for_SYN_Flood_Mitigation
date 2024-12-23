# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the TCP Server Python script into the container
COPY tcp-server.py /app/tcp-server.py

# Expose the port the TCP server will listen on
EXPOSE 8080

# Command to run the TCP server script
CMD ["python3", "tcp-server.py"]
