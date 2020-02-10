class: Workflow
cwlVersion: v1.0
id: normalizeoningest
label: normalizeOnIngest
$namespaces:
  sbg: 'https://www.sevenbridges.com/'
inputs:
  - id: in-url
    type: string
    'sbg:x': 0
    'sbg:y': 0
  - id: out-url
    type: string
outputs: []
steps:
  - id: extract
    in:
      - id: url
        source: in-url
    out:
      - id: UnNormalized
    run: ./extract.cwl
    'sbg:x': 97
    'sbg:y': 0
  - id: normalize
    in:
      - id: UnNormalized
        source: extract/UnNormalized
    out:
      - id: normalized
    run: ./normalize.cwl
    label: Normalize
    'sbg:x': 311.921875
    'sbg:y': 0
  - id: upload
    in:
      - id: normalized
        source: normalize/normalized
      - id: normalizedPath
        source: out-url 
    out: []
    run: ./upload.cwl
    'sbg:x': 589.671875
    'sbg:y': 0
