# Use the latest Ubuntu image as base
FROM ubuntu:latest

# Set environment variables to non-interactive to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3 and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && apt-get clean

# Install required Python packages (if any, for example)
# RUN pip3 install some_package

# Set the working directory inside the container
WORKDIR /app

# Copy your Python files to the container
COPY . /app

# Run the user-client script when the container starts
CMD ["python3", "user-client.py"]
