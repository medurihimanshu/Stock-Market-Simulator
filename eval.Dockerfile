# Stage 1 Base Image
FROM python:3.11-slim

WORKDIR /app

# Stage 2: Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Copy the app
COPY . .

# Stage 4: Expose the port and run the app
EXPOSE 8000

EXPOSE 5432

CMD ["uvicorn", "assessment_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 5: Run the tests
CMD ["mkdir", "-p", "/app/output"]
CMD ["bash", "execute_tests.sh"]