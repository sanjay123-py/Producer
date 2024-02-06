FROM python:3.8
RUN mkdir producer
COPY . /producer/
WORKDIR /producer
RUN apt update -y && apt install awscli -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "producer_main.py"]