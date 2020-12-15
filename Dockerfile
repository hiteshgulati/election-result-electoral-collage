FROM python:3.8.6-slim-buster

#Make Directory for Application
WORKDIR /app

#Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy Source Code
COPY /dashboard .

EXPOSE 8080

#Run Application
CMD [ "python","app.py" ]