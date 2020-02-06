class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
hints:
  DockerRequirement:
    dockerPull: mcconfiged
baseCommand:
  - mc
  - cp
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
