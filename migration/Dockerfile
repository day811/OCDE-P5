FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY migration_script.py .
CMD ["python", "migration_script.py"]