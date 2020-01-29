FROM python:3.7.3
RUN pip install flask
RUN pip install requests
RUN pip install minio
RUN pip install wes-service
COPY listener.py /srv/
COPY tests /
#The alternative to this copy line is to prepend all local workflow file paths with "srv/tests/"
ENTRYPOINT [ "python", "/srv/listener.py"]
