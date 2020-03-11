class: CommandLineTool
cwlVersion: v1.0
# hints:
#   DockerRequirement: # Required if we do python approach, not if we do curl and pass --data
#     dockerPull: ga4gh-dos
baseCommand: curl
inputs:
  - id: data # This may need ' ' around it because of spaces, if so just put ' ' in the string in listener
    type: string # Use listener to consolidate all data into a string
    inputBinding:
      position: 2
      prefix: '--data'
  - id: url
    type: string
    inputBinding:
      position: 3
outputs: []
arguments:
  - position: 0
    prefix: '-X'
    valueFrom: POST
  - position: 1
    prefix: '-H'
    valueFrom: "Content-Type: application/json"
