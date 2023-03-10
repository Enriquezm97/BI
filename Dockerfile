FROM python:3.9

#COPY . /usr/src/app
#WORKDIR 
WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -U pip

RUN pip install mysql-connector-python

RUN pip install -r requirements.txt 


COPY . .

EXPOSE 8000

RUN pip --version

#CMD [ "python","manage.py","runserver"]

CMD [ "python","manage.py","runserver","0.0.0.0:8000"]

