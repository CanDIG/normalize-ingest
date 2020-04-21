class: CommandLineTool
cwlVersion: v1.0
hints:
  DockerRequirement:
    dockerPull: minio/mc:latest
  EnvVarRequirement:
    envDef: 
      MC_HOST_minio: http://$(inputs.access):$(inputs.secret)@$(inputs.domain):$(inputs.port)
baseCommand: cp
inputs:
  - id: url
    type: string
    inputBinding:
      position: 1
  - id: access
    type: string
  - id: secret
    type: string
  - id: domain
    type: string
  - id: port
    type: string
outputs:
  - id: UnNormalized
    type: File
    outputBinding:
      glob: '*.vcf.gz'
arguments:
  - position: 2
    prefix: ''
    separate: false
    valueFrom: .