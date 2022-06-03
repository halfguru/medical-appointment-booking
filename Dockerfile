FROM python:3.9.5-slim

LABEL maintainer="Simon HO <simon.ho@gmail.com>" \
    description="Medical appointment REST server"

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /

WORKDIR /
CMD ["python", "app/app.py"]