FROM python:3.10

WORKDIR /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["uvicorn", "devops_project.main:app", "--host", "0.0.0.0", "--port", "80"]