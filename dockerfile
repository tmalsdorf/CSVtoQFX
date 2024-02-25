# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY app/. .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV APP_NAME="csvtopdf"
ENV FLASK_ENV=production

# Use Gunicorn as the entry point
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
