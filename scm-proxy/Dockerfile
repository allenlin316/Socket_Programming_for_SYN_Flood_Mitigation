# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tcpdump \
    && rm -rf /var/lib/apt/lists/* \
    && ln /bin/tcpdump /tmp/static-tcpdump \
    && apt-get clean

# Copy the SCM Proxy Python script into the container
COPY scm-proxy.py /app/scm-proxy.py

# Expose the port the SCM proxy will listen on
EXPOSE 9090

# Command to run the SCM proxy script
CMD ["python3", "scm-proxy.py"]
