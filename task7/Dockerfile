FROM python:3.12
WORKDIR /usr/src/task5_6 
COPY src/api.py .
COPY src/database.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "1111"]