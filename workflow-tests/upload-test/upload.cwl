class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
hints:
  DockerRequirement:
    dockerPull: mcconfiged
baseCommand:
  - mc
inputs:
  - id: normalized.vcf
    type: File
    inputBinding:
      position: 1
outputs: []
label: Upload
arguments:
  - position: 0
    prefix: ''
    separate: false
    valueFrom: cp
  - position: 2
    prefix: ''
    separate: false
    valueFrom: minio/samples/processed
