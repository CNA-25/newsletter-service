FROM python:3.10

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set default environment to production
ENV MODE=production

# Expose port 8080
EXPOSE 8080

# Start FastAPI correctly
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
