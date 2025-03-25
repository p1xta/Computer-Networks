FROM python:3.12
WORKDIR /usr/src/task5_6 
COPY api.py .
COPY database.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "1111"]