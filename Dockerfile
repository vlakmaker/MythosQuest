# Use the official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask web app
EXPOSE 5000

# Use environment variables from .env
ENV PYTHONUNBUFFERED=1

# Run the AI Dungeon Master app
CMD ["python", "ai_dm.py"]
