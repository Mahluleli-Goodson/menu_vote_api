FROM python:3.7

# Set the working directory in container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code to the container
COPY . .

# Run database migrations
RUN python manage.py migrate

# Load fixtures (if applicable)
RUN python manage.py loaddata menu_scores/fixtures/scores.json

# Expose Django port
EXPOSE 8000

# Define the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
