FROM python:3.14-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libjpeg-dev
    # pip install --upgrade pip && \  
    # pip install -r requirements.txt

WORKDIR /app

COPY requirements.txt .

RUN  pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn","app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

