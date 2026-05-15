FROM python:3.11-slim

WORKDIR /app

# Copy requirements FIRST
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project AFTER dependencies
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "Backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]