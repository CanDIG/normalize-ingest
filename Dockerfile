FROM python:3.7.6
RUN pip install flask
RUN pip install requests
RUN pip install minio
RUN pip install wes-service
RUN apt-get update && apt-get install -y \
	samtools bcftools vim nano
COPY listener.py /srv/listener.py
WORKDIR /srv
ENTRYPOINT [ "python", "/srv/listener.py"]
