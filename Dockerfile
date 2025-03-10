# Use an official lightweight Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure Ollama is installed
RUN pip install ollama

# Copy all project files to the container
COPY . .

# Expose Flask's port
EXPOSE 5000

# Start Flask directly
CMD ["python", "ai_dm.py"]
