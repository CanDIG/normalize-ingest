class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
id: bashtool
baseCommand:
  - sh
inputs:
  - id: bashFile
    type: File
    inputBinding:
      position: 1
outputs:
  - id: UnNormalized
    type: File
    outputBinding:
      glob: NA18537.vcf.gz
label: BashTool
