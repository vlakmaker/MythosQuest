# Use official Python image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Command to run the script
CMD ["python", "ai_dm.py"]
