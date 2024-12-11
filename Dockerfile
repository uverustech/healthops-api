FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py migrate

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--config", "config/gunicorn/prod.py", "healthops.wsgi:application"]

