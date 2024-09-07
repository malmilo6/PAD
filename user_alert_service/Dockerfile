FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
