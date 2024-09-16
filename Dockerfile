# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir sympy numpy

# Expose the port
EXPOSE 65432

# Default command to run the server
CMD ["python3", "server.py"]