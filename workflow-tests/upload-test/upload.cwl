class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
hints:
  DockerRequirement:
    dockerPull: minio/mc
  EnvVarRequirement:
    envDef: 
      MC_HOST_minio: http://miniotest:miniotest@host.docker.internal:9000
baseCommand: cp
inputs:
  - id: normalized.vcf
    type: File
    inputBinding:
      position: 1
outputs: []
arguments:
  - position: 2
    prefix: ''
    separate: false
    valueFrom: minio/samples/processed
