FROM python:3.12

WORKDIR /

COPY requirements.txt ./

RUN pip install -r requirements.txt --break-system-packages

COPY . .

CMD [ "python3", "main.py" ]