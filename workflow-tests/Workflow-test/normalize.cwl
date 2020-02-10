class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: normalize
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
      glob: '*'
label: Normalize
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
