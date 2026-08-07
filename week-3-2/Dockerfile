FROM python:3.10-slim

# Prevent Python from writing pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Install dependencies first
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy all project files into /app
COPY . .

# Expose port 8000
EXPOSE 8000

# Start Uvicorn
CMD ["python", "-m", "uvicorn", "CRUD_API:app", "--host", "0.0.0.0", "--port", "8000"]