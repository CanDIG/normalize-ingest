# Procedure to Test Minio to WES Server connection for Normalize on Ingest Pipeline

## Prerequisites
```bash
#Install WES server and client
pip install wes-service
#Install Toil with cwl-runner, you can skip this if you already have cwl-runner and cwltool
pip install toil git+git://github.com/common-workflow-language/workflow-service
```
## Start minio

```bash
docker run --rm -d --name minio -e "MINIO_ACCESS_KEY=x_key" -e "MINIO_SECRET_KEY=x_secret" --rm -it -p 9000:9000  minio/minio server /data
```
You may omit '-d' to run in foreground and/or change the authentication keys to your desire

## Set up Minio Webhook
We will add a bucket to the server and configure it with a webhook event targeted at port 8082.
```bash
#Add credentials to minio client
./mc config host add myminio http://localhost:9000 x_key x_secret --api S3v4
#Create json-files bucket
./mc mb myminio/json-files

#Configure webhook
./mc admin config set myminio notify_webhook:1 queue_limit="0"  endpoint="http://host.docker.internal:8082/listener" queue_dir=""
#Restart minio
./mc admin service restart myminio
#Enable bucket notification on json-files
./mc event add myminio/json-files arn:minio:sqs::1:webhook --event put --suffix .json

#Check if Webhook is configured
./mc event list myminio/json-files
#Expected output
arn:minio:sqs::1:webhook   s3:ObjectCreated:*   Filter: suffix=".json"
```
## Run WES-Server and Listener
We will run the WES server and the Listener in the foreground on seperate terminals to test both of their .behaviors
```bash
#Start wes-server in a terminal
wes-server --backend=wes_service.cwl_runner --opt runner=cwltoil --opt extra=--logLevel=CRITICAL
#Start Listener in a different terminal
python Listener.py
```
## Test Listener
We will create a test file.json in our current directory and send it to minio to trigger the webhook event, then monitor outputs.
```bash
#Create payload:
echo '{"id": 001, "name": "ruan", "surname": "bekker"}' > file.json
#Send file to minio to trigger webhook event
./mc cp file.json myminio/json-files/234098234092834092834.json

#Expected Listener Output
127.0.0.1 - - [21/Jan/2020 10:37:45] "POST /listener HTTP/1.1" 406 -
127.0.0.1 - - [21/Jan/2020 10:37:45] "POST /listener HTTP/1.1" 200 -

#Expected WES Output
INFO:root:Workflow None: Using workflow_url 'https://dockstore.org:8443/api/ga4gh/v2/tools/quay.io%2Fbriandoconnor%2Fdockstore-tool-md5sum/versions/master/plain-CWL/descriptor/%2FDockstore.cwl'
INFO:werkzeug:127.0.0.1 - - [21/Jan/2020 10:40:43] "POST /ga4gh/wes/v1/runs HTTP/1.1" 200 -

#Test Workflow Creation
python ListWorkflows.py
#Expected Output Format
{
  "next_page_token": "",
  "workflows": [
    {
      "run_id": "cb2f8aa1db054ec08ac96fa9b43387c3",
      "state": "EXECUTOR_ERROR"
    }
  ]
}
```
The exact run_id and state of the workflow will vary.
