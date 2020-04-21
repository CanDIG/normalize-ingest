class: CommandLineTool
cwlVersion: v1.0
hints:
  DockerRequirement:
    dockerPull: biocontainers/bcftools:v1.9-1-deb_cv1
baseCommand:
  - bcftools
inputs:
  - id: UnNormalized
    type: File
    inputBinding:
      position: 2
outputs:
  - id: normalized
    type: File
    outputBinding:
      glob: '*.vcf'
arguments:
  - position: 0
    prefix: ''
    separate: false
    valueFrom: norm
  - position: 1
    prefix: '-d'
    valueFrom: all
  - position: 3
    prefix: '-o'
    valueFrom: $(inputs.UnNormalized.nameroot)
