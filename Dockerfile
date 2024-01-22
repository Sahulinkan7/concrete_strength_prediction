FROM python:3.11.5-alpine

WORKDIR /concrete_strength_prediction

COPY . .

RUN pip3 install -r requirements.txt

