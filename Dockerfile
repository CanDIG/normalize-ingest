FROM python:3.7.3
RUN pip install flask
RUN pip install requests
RUN pip install minio
RUN pip install wes-service
COPY listener.py /srv/listener.py
ENTRYPOINT [ "python", "/srv/listener.py"]
