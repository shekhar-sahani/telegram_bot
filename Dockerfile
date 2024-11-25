# Use a Python base image with the required version (e.g., python:3.10)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the necessary Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (including config.py) into the container
COPY . /app/

# Expose the port the app will run on (optional)
EXPOSE 8000

# Define the command to run your bot
CMD ["python", "gemini_bot_2.py"]
