# Normalize on Ingest Project Plan

## Overview


## Workflow

![Project Workflow](assets/workflow.png "workflow diagram")

## Task list

- [✓] Evaluate methods of MinIO bucket notification
- [✓] Create PoC of MinIO webhooks
- [✓] Build listener service to receive bucket notification
- [✓] Use notification to trigger workflow
- [ ] Create a normalization CWL workflow
  - [ ] Use inputs from S3/MinIO
  - [ ] Run  htsfile  to retrieve sample
  - [ ] Run  bcftools norm  on  file.vcf.gz
  - [ ] Run  mc cp  to put processed file into minio/samples/processed/file.vcf
- [✓] Create demo presentation
  - [✓] Run  docker-compose
  - [✓] Setup buckets
  - [✓] Enable debugging for services
  - [✓] Add sample files
  - [✓] Ingest should run successful pipeline
  - [✓] diff the output between two files
- [ ] Expand PoC with DRS
- [ ] Add ability to run workflow over WES

## Gantt Chart

```mermaid
gantt
  title Project Timeline
  dateFormat YYYY-MM-DD

  section Initial PoC
    Evaluate methods of MinIO bucket notification :a1, 2019-12-06, 3w
    Evaluate methods to run serverless functions/lambdas :a2, after a1, 3w
    Present MVP process :a3, after a2, 1w

  section Create Listener Service
    Trigger automated actions to occur based on bucket notification :b2, after b1, 1w

  section Develop CWL Workflow

  section Run Workflows via WES

  section Track Providence with DRS

```
