#Short file to check currently running workflows
import requests
req = requests.get('http://127.0.0.1:8080/ga4gh/wes/v1/runs')
print(req.text)