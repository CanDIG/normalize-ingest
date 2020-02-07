class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
baseCommand:
  - python
inputs:
  - id: input
    type: File?
    inputBinding:
      position: 0
outputs:
  - id: UnNormalized
    type: File
    outputBinding:
      glob: NA18537.vcf.gz
label: TestPythonTool
