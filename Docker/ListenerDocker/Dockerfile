FROM python:3.6.0
COPY . .
RUN pip install flask
RUN pip install requests
RUN pip install minio
RUN pip install wes-service
CMD [ "python", "./Listener.py"]
