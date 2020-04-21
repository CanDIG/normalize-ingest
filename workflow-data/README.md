# Quick tests for CWL Tools and Workflow
The workflow has 4 tools, extract, normalize, upload and drs. The workflow takes a path to a .vcf.gz file in minio and a path to a final directory folder. It then downloads the .vcf.gz file, normalizes it using bcftools norm, uploads the normalized file into a given minio output folder with its original name appended with "-normalized.vcf", and updates DRS. Each of the tools can be tested individually with their corresponding jobs in their folders, except for the drs tool.
## 1) Extract tool
Retrieves the .vcf.gz file from minio thus minio must be running during this test. The default input path in the job file is minio/samples/unprocessed/NA18537.vcf.gz
```bash
#Run Tool
cwl-runner extract.cwl extract-job.json
```
## 2) Normalize tool
Takes input .vcf.gz file and normalizes, the job file is set to normalize NA18537.vcf.gz for this test but is linked to the output of extract in the actual workflow.
```bash
#Run Tool
cwl-runner normalize.cwl normalize-job.yml
```
## 3) Upload tool
Uploads the normalized file to minio, so minio needs to be running during this test. The job file specifies to send the normalized.vcf file for this test but in the actual workflow it is linked to the output of the normalize tool. The destination of the file is set to minio/samples/processed for this test but can also be changed from the job file
```bash
#Run Tool
cwl-runner upload.cwl upload-job.cwl
```
## Complete Workflow
Uses the extract, normalize and upload tool. Minio must be running and the job file path of the input file, currently minio/samples/unprocessed/NA18537.vcf.gz to minio/samples/processed/NA18537-normalized.vcf
```bash
#Run Workflow
cwl-runner normalizeoningest.cwl inputjob.json
```