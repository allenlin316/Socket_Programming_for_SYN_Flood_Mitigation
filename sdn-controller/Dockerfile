# Use Ubuntu as the base image
FROM ubuntu:latest

# Set the working directory inside the container
WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy the SDN Controller Python script into the container
COPY sdn-controller.py /app/sdn-controller.py

# Expose the port the SDN controller will listen on
EXPOSE 8082

# Command to run the SDN controller script
CMD ["python3", "sdn-controller.py"]
