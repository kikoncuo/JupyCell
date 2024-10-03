# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements.txt file to the container at /app
COPY requirements.txt requirements_app.txt .

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Install any needed packages for the interpreter specified in requirements_app.txt
RUN pip install --no-cache-dir -r requirements_app.txt

# Step 6: Copy the rest of the application code to the container
COPY . .

# Step 7: Expose port 8000 to the outside world
EXPOSE 8000

# Step 8: Run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
