# Normalize on Ingest Pipeline Proceedure

## Start minio

```bash
docker run --rm --name minio --rm -it -p 9000:9000  minio/minio server /data
```

## Configure minio server with webhook

```bash
# add credentials to minio client
mc config host add myminio http://localhost:9000 x_key x_secret --api S3v4

# create backup of server config
mc mb myminio/json-files
mc admin config get myminio > config.json
```

### Append the webhook config to server config

```bash
KEY:
notify_webhook[:name]  publish bucket notifications to webhook endpoints

ARGS:
endpoint*    (url)       webhook server endpoint e.g. http://localhost:8080/minio/events
auth_token   (string)    opaque string or JWT authorization token
queue_dir    (path)      staging dir for undelivered messages e.g. '/home/events'
queue_limit  (number)    maximum limit for undelivered messages, defaults to '10000'
comment      (sentence)  optionally add a comment to this setting
```
```json
"webhook":{"1":{"enable":true,"endpoint":"http://192.168.0.104:8082","queueDir":"","queueLimit":0}}}
```

### Alternatively, create webhook via docker

```bash
MINIO_NOTIFY_WEBHOOK_ENDPOINT*    (url)       webhook server endpoint e.g. http://localhost:8080/minio/events
MINIO_NOTIFY_WEBHOOK_AUTH_TOKEN   (string)    opaque string or JWT authorization token
MINIO_NOTIFY_WEBHOOK_QUEUE_DIR    (path)      staging dir for undelivered messages e.g. '/home/events'
MINIO_NOTIFY_WEBHOOK_QUEUE_LIMIT  (number)    maximum limit for undelivered messages, defaults to '10000'
MINIO_NOTIFY_WEBHOOK_COMMENT      (sentence)  optionally add a comment to this setting
```

## Set config

```bash
mc admin config set myminio < config.json
mc admin service restart myminio
```

## Add event subsciption

```bash
mc event add myminio/json-files arn:minio:sqs::1:webhook --event put --suffix .json
mc event list myminio/json-files
arn:minio:sqs::1:webhook   s3:ObjectCreated:*   Filter: suffix=".json"
```

## Create Listener/WES Runner

```python
from flask import Flask, request, jsonify
from minio import Minio

client = Minio('127.0.0.1:9000', access_key='x', secret_key='x', secure=False)
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def main():
    payload = request.get_json()
    a = client.get_object('json-files', payload['Records'][0]['s3']['object']['key'])
    print(a.read())
    return jsonify(payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)

# TODO: import wes-client code and submit workflow
# TODO: ue python to run bcftools norm in process
```

## Create Normalize on Ingest Workflow

```cwl
#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
label: CanDIG normalize-on-ingest pipeline
doc: |
  # TODO: add documentation

#requirements:
#  InlineJavascriptRequirement: {}
hints:
  SoftwareRequirement:
   packages:
     - package: samtools 
       version: [ "0.1.19" ]
       # specs: []
  #DockerRequirement
  #  dockerPull: hive/heptagon/1.1
  # TODO: create docker-requirement for samtools

inputs:
# TODO: specify inputs

outputs:
# TODO: specify output
```
create payload:

echo '{"id": 001, "name": "ruan", "surname": "bekker"}' > file.json

copy to minio:

mc cp file.json myminio/json-files/234098234092834092834.json

Flask output:

192.168.0.104 - - [11/Jul/2019 23:36:07] "POST / HTTP/1.1" 200 -
{"id": 001, "name": "ruan", "surname": "bekker"}
## References
[Minio Bucket Notification Guide](https://docs.min.io/docs/minio-bucket-notification-guide.html)
