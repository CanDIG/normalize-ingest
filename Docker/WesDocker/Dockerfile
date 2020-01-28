FROM ubuntu:latest
RUN apt update
RUN apt -y install python-pip
RUN pip install cwl-runner
RUN pip install wes-service
CMD wes-server
