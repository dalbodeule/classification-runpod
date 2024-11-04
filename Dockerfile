FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that the server will run on
EXPOSE 8000

# Set environment variable for the model name
ENV MODEL_NAME="google-bert/bert-base-uncased"

# Run the server
CMD ["python", "-u", "main.py"]