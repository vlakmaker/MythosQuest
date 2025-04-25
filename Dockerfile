FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure run.py and related scripts are executable if needed
# RUN chmod +x run.py

EXPOSE 5000

# Set non-root user? (Good practice, optional for simplicity now)
# RUN useradd -m myuser
# USER myuser

CMD ["python", "run.py"]