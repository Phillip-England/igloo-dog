# Use an official Python image that is compatible with Railway
FROM python:3.8

# Set a working directory
WORKDIR /app

# Copy your application code and requirements file
COPY . /app

# Install your application's dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which your FastAPI app will run (modify it if your app uses a different port)
EXPOSE 8000

# Change the working directory to your FastAPI app's source code directory
WORKDIR /app/src

# Use uvicorn to start your FastAPI app (modify the entry point if necessary)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]