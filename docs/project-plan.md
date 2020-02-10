# Normalize on Ingest Project Plan

## Overview


## Workflow

```mermaid
graph LR
  subgraph Step1 - Configure MinIO Server for Bucket Notification
    mc[minio client] -->|configure bucket notification| ms[(minio server)]
    ms -->|bucket for unprocessed vcfs| b1[/unprocessed]
    ms -->|bucket for normalized vcfs| b2[/processed]
  end
  subgraph Step2 - Client Submission of Data
    cl[client] -->|upload of vcf| ms
  end
  subgraph Step3 - 
  wf[workflow]
  drs[drs server]
  wes[wes server]
  hpc[hpc service]

  mc-. setup of server .->ms

```


## Task list


## Gantt Chart

```mermaid
gantt
title Project Timeline
dateFormat YYYY-MM-DD

section Minimal Viable Product

```
