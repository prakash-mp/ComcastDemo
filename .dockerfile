# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app/app

# Copy the entire app directory into the container
COPY ./app .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH environment variable to /app
ENV PYTHONPATH=/app

# Expose port 8000
EXPOSE 8000

# Make the prestart.sh script executable
RUN chmod +x prestart.sh

# Run the prestart.sh script when the container starts
ENTRYPOINT ["/bin/sh","/app/app/prestart.sh"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
