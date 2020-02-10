# Quick tests for CWL Tools and Workflow
The workflow has 3 tools, extract, normalize and upload. The workflow takes a path to a .vcf.gz file in minio, downloads the file, normalizes it using bcftools norm, and uploads the normalized file into minio/samples/processed with its original name except unziped. Each of the tools can be tested individually with their corresponding jobs.
## 1) Extract tool
Retrieves the .vcf.gz file from minio so minio must be running during this test. The default input path in the job file is minio/samples/unprocessed/NA18537.vcf.gz
```bash
#Run Tool
cwl-runner extract.cwl extract-job.json
```
## 2) Normalize tool
Takes input .vcf.gz file and normalizes, the job file is set to normalize NA18537.vcf.gz for this test but is linked to the output of extract in the actual workflow.
```bash
cwl-runner normalize.cwl normalize-job.yml
```
## 3) Upload tool
Uploads the normalized file to minio, so minio needs to be running during this test. The job file specifies to send the normalized.vcf files for this test but in the actual workflow it is linked to the output of the normalize tool. 
```bash
cwl-runner upload.cwl upload-job.cwl
```
## Complete Workflow
Uses the extract, normalize and upload tool. Minio must be running and the job file path of the input file, currently minio/samples/unprocessed/NA18537.vcf.gz.
```bash
cwl-runner normalizeoningest.cwl inputjob.json
```
## Overall Issues
1) The name of the normalized file is currently the same as the input file except without ".gz".
2) The credentials that the extract and upload tools use are miniotest miniotest. For now we want these to come from environment variables instead of being hard coded.