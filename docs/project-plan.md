# Normalize on Ingest Project Plan

## Overview


## Workflow

```mermaid
graph TB

  subgraph Step1
    mc[minio client] -->|configure bucket notification| ms[(minio server)]
    ms -.-|unprocessed vcfs| b1["/minio/samples/unprocessed"]
    ms -.-|normalized vcfs| b2["/minio/samples/processed"]
  end

  subgraph Step2
    cl[client] -->|upload of vcf| ms
  end



  subgraph Step3
    ms -->|send webhook| ls[listener]
    ls -->|trigger 'bcf-norm' workflow| wes[wes server]
    wes -->|convert CWL into compatible steps| hpc[hpc/executor service]
    b1 -->|pull copy of unprocessed vcf| hpc
    hpc -->|put 'normalized' vcf back into minio| b2
  end

  subgraph Step4
    ls -->|trigger 'update drs' workflow| wes
    hpc -->|add DRS dataobject record| drs[drs server]
  end
```


## Task list


## Gantt Chart

```mermaid
gantt
title Project Timeline
dateFormat YYYY-MM-DD

section Minimal Viable Product

```
