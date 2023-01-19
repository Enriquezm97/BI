FROM python:3.9.0

#COPY . /usr/src/app
#WORKDIR 
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

COPY . .

EXPOSE 8080

CMD [ "python","manage.py","runserver","0.0.0.0:8080"]