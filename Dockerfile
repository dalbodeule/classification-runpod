FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py /app/

# Set environment variable for the model name
ENV MODEL_NAME="google-bert/bert-base-uncased"

# Run the server
CMD ["python", "-u", "/app/main.py"]