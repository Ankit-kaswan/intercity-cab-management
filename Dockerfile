# Stage 1 Base Image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Stage 2: Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Copy the app
COPY . .

# Stage 4: Expose the port and run the app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
