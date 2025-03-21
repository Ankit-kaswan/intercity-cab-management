# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the project files
COPY . .

ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt

# Run tests with coverage report
CMD ["pytest", "--cache-clear", "--disable-warnings", "--cov=app", "--cov-report=html"]
