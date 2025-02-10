# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

#Collect static files
#RUN python manage.py collectstatic --noinput
# Expose port 8000 to the outside world
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run the application
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "savannaEcommerceDjango.wsgi.application"]