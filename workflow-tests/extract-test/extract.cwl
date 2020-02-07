class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
hints:
  DockerRequirement:
    dockerPull: minio/mc:latest
  EnvVarRequirement:
    envDef: 
      MC_HOST_minio: http://miniotest:miniotest@host.docker.internal:9000
baseCommand: cp
inputs:
  - id: url
    type: string
    inputBinding:
      position: 1
outputs:
  - id: UnNormalized.vcf.gz
    type: File
    outputBinding:
      glob: '*.vcf.gz'
arguments:
  - position: 2
    prefix: ''
    separate: false
    valueFrom: .
