# Use the official Python image as the base image
FROM python:3.10.11

# Set the working directory in the container
WORKDIR /videoclub

# Copy the application files into the working directory
COPY . /videoclub

# Install the application dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the project files
COPY . .

# TCP PORT
EXPOSE 8000

# Define the entry point for the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

