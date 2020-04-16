FROM python:3.7.6
RUN pip install flask
RUN pip install requests
RUN pip install minio
RUN pip install werkzeug==0.16.1
RUN pip install connexion==1.4.2
RUN pip install wes-service
WORKDIR /srv
ENTRYPOINT [ "python", "/srv/listener.py"]
