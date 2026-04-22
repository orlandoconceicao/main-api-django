FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/software_sales

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]