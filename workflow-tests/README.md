# Quick tests for CWL 
## 1) Docker example tool
```bash
#Run Tool
cwl-runner docker.cwl docker-job.yml
```
This works, it is able to pull the node:slim image and run node command from there
## 2) Extract tool using mcconfiged image
Retrieves the .vcf.gz file from minio so minio must be running during this test with NA18537.vcf.gz in the samples/unprocessed bucket. Currently it uses mc cp.
```bash
#Create image
docker build -t mcconfiged .
#Run Tool
cwl-runner extract.cwl extract-job.json
```
This current results in a Job Error, leading me to believe that the mc cp command fails to complete most likely due to a connection error between the mcconfiged container and minio. This could probably be because the DockerFile is not set up correctly. 
## 3) Normalize tool
Takes input NA18536.vcf.gz file and normalizes, do not need to generalize because when a workflow combines the tools we just have to match ids and delete the previous job files
```bash
cwl-runner normalize.cwl normalize-job.yml
```
This actually works!
## 4) Upload tool
Uploads the normalized.vcf file to minio, so minio needs to be running during this test
```bash
cwl-runner upload.cwl upload-job.cwl
```
Currently uses mc cp and suffers from the same imaging error as extract
## 5) Bash file test
This is a bash implemntation of the extract tool, so minio needs to be running with NA18537.vcf.gz in samples/unprocessed
```bash
cwl-runner --debug bashtool.cwl bashjob.yml
```
The fact that this works is why I am confident the issue with the other extract tool is config. But I don't like this 'solution' because I think it undermines the point of having a workflow in the first place. Which is why I think making an mc configured docker image to run mc cp out of is the way to go.

## Overall Issues
### 1)
There is need to make a docker image that has minio client configured with: mc config host add minio http://127.0.0.1:9000 miniotest miniotest --api S3v4
The current DockerFile in extract-test/ is not configuring mc properly
### 2)
Once all the tools work individually, a workflow will need to be made to combine all of them