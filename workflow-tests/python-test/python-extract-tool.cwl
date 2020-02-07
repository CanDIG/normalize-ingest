class: CommandLineTool
cwlVersion: v1.0
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
baseCommand:
  - python
inputs:
  - id: pyfile
    type: File
    inputBinding:
      position: 0
  - id: minio-path
    type: string
    inputBinding:
      position: 1
outputs:
  - id: UnNormalized
    type: File
    outputBinding:
      glob: '*.vcf.gz'
label: TestPythonTool
