# прописываются образы для подготовки контейнера
FROM python:3.8.5
COPY . /my_app
WORKDIR /my_app
RUN pip install -r requirements.txt