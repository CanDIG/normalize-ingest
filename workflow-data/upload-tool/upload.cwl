class: CommandLineTool
cwlVersion: v1.0
hints:
  DockerRequirement:
    dockerPull: minio/mc
  EnvVarRequirement:
    envDef: 
      MC_HOST_minio: http://$(inputs.access):$(inputs.secret)@$(inputs.domain):$(inputs.port)
baseCommand: cp
inputs:
  - id: normalized
    type: File
    inputBinding:
      position: 1
  - id: normalizedPath
    type: string
  - id: access
    type: string
  - id: secret
    type: string
  - id: domain
    type: string
  - id: port
    type: string
outputs: []
arguments:
  - position: 2
    prefix: ''
    separate: false
    valueFrom: $(inputs.normalizedPath)/$(inputs.normalized.nameroot)-normalized$(inputs.normalized.nameext)