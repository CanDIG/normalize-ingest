import requests
import json
from flask import Flask, request, jsonify
from minio import Minio

#Access the Minio server if needed, access keys may vary based on minio config
#client = Minio('127.0.0.1:9000', access_key="minioadmin", secret_key="minioadmin", secure=False)

app = Flask(__name__)
@app.route('/listener', methods=['POST'])
def main():
    #Minio events result in two calls, so we ignore the first
    if not request.data:
        return "First Request Ignored", 406

    #Retrieve Workflow Data from workflowInput.json
    inFile = open("workflowInput.json", "r")
    if inFile.mode == "r":
        param = inFile.read()
    param = json.loads(param)

    #Check if input workflow_url was a name to be given to dockstore
    if param["workflow_url/name"][:4] != "http":
        #Get the workflow_url from dockstore to send to wes-server
        response = requests.get('https://dockstore.org:8443/api/ga4gh/v1/tools/', params={"name": param["workflow_url/name"]})
        url = response.json()[0]['versions'][0]['url'] + '/plain-CWL/descriptor/%2FDockstore.cwl'
        param['workflow_url/name'] = url

    #Check if input params needs to be retrieved from local file
    if isinstance(param["workflow_params/json_path"], str):
        inFile2 = open(param["workflow_params/json_path"], "r")
        #Set workflow_param
        if inFile2.mode == "r":
            param['workflow_params/json_path'] = inFile2.read()
    else:
        param['workflow_params/json_path'] = json.dumps(param['workflow_params/json_path'])

    #Fix key naming for request
    param["workflow_params"] = param.pop("workflow_params/json_path")
    param["workflow_url"] = param.pop("workflow_url/name")
    #Make the request, req.text holds the wes workflow id
    req = requests.post('http://127.0.0.1:8080/ga4gh/wes/v1/runs', data=param)

    return "Workflow Request Sent"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
# TODO: ue python to run bcftools norm in process
# TODO: Generalize input workflow further