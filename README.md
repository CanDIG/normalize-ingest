# Procedure to Test Minio to WES Server connection for Normalize on Ingest Pipeline

## Prerequisites
- Docker and Docker-Compose are required. They can be installed from https://docs.docker.com/get-docker/ and https://docs.docker.com/compose/install/ respectively.
- Minio Client is also required, it can be installed following the instructions on https://docs.min.io/docs/minio-client-complete-guide.html

## Start Services
Before starting the services, check the .env file and change any of the environment variables to suit your needs. Docker-compose will automatically use this file when you run the next command. DOS variables are included but the default repository service is CHORD's DRS implementation.  
```bash
# Build and Start all services in docker-compose.yml
docker-compose up -d
```
You may omit `-d` to run in foreground.  
Once the services are running, Run the short shell script `mc-config.sh` via
```bash
# Configure minio buckets and webhook event
./mc-config.sh
```
This does some basic set up of buckets and authentication for minio based on environment variables
## Test Process
We will test the process by uploading `workflow-data/normalize-tool/NA18537.vcf.gz` to `minio/samples/unprocessed/`. This can be done through the minio UI running on `http://$MINIO_DOMAIN:MINIO_UI_PORT/minio/samples/unprocessed`. Find the `+` button and upload the file.  
After a delay, the expected results are:  
- A completed workflow should be listed on `http://localhost:$WES_PORT/ga4gh/wes/v1/runs`
- A `NA18537-normalized.vcf` file should have been added to `http://\$MINIO_DOMAIN:MINIO_UI_PORT/minio/$MINIO_PROCESSED_DIR`
- A DRS related file should have been added to `http://\$MINIO_DOMAIN:MINIO_UI_PORT/minio/$MINIO_DRS_BUCKET`
# Overview of Services and Technical Notes
## Functionality
This pipeline is accomplished by having a minio webhook event trigger on ingest and send a request to a listener service which is a basic Flask endpoint.  

The listener collects data from the webhook about the file added, from workflowInput.json about the workflow to run, and from environment variables about the inputs to the workflow. It then gathers this data and uses the wes_client library to make a post request to WES server.  

WES accepts the request and uses cwltool to run the given workflow. The workflow in this example retrieves the inputed file from minio, runs bcftools norm on it, returns the normalized file too minio, and updates DRS accordingly.

## Development Notes
- The listener is where the inputs to the workflow are finalized before being sent to WES. If you want to submit a different workflow, modify workflowInput.json with your new workflow and corresponding attachments, then ensure that the job creation in the listener is changed as well.
- Cwltool has been inconsistent at times, switching to toil should be considered if faced with strange errors such as workflows magically starting up again.
- The tools used the the workflow can be found in their folders in the workflow-data/ directory. Each of their folders come with the necessary files to test them independently of the overall workflow with the exception of the DRS tool.
- If adding environment variables for any purpose, remember to add them to the proper services in the docker-compose file so the service that needs the variable actually has it.
- The default set up uses host.docker.internal, which is only supported on OS X and Windows, so this currently does not support Linux. Implementing Traefik is currently planned solution.
- The Dockerfiles for built services are in the directories under `docker-files`