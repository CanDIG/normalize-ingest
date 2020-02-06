class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: normalize
baseCommand:
  - bcftools
inputs:
  - id: UnNormalized.vcf.gz
    type: File
    inputBinding:
      position: 2
outputs:
  - id: normalized.vcf
    type: File
    outputBinding:
      glob: normalized.vcf
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
    valueFrom: normalized.vcf
