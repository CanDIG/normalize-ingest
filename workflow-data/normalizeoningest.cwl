class: Workflow
cwlVersion: v1.0
inputs:
  - id: in-url
    type: string
  - id: out-url
    type: string
  - id: minio-access
    type: string
  - id: minio-secret
    type: string
  - id: minio-domain
    type: string
  - id: minio-ui-port
    type: string
  - id: in-drs-data
    type: string
  - id: in-drs-url
    type: string
outputs: []
steps:
  - id: extract
    in:
      - id: url
        source: in-url
      - id: access
        source: minio-access
      - id: secret
        source: minio-secret
      - id: domain
        source: minio-domain
      - id: port
        source: minio-ui-port
    out:
      - id: UnNormalized
    run: extract-tool/extract.cwl
  - id: normalize
    in:
      - id: UnNormalized
        source: extract/UnNormalized
    out:
      - id: normalized
    run: normalize-tool/normalize.cwl
  - id: upload
    in:
      - id: normalized
        source: normalize/normalized
      - id: normalizedPath
        source: out-url
      - id: access
        source: minio-access
      - id: secret
        source: minio-secret
      - id: domain
        source: minio-domain
      - id: port
        source: minio-ui-port
    out:
      - id: fakeOutput
    run: upload-tool/upload.cwl
  - id: drs
    in:
      - id: data
        source: in-drs-data
      - id: url
        source: in-drs-url
      - id: fakeInput
        source: upload/fakeOutput
    out: []
    run: updateDRS-tool/drs.cwl