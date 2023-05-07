FROM python:3.8

WORKDIR /app

COPY requirements.txt setup.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

COPY financial/ /app/financial

CMD ["uvicorn", "financial.app:app", "--host", "0.0.0.0", "--port", "5000"]
