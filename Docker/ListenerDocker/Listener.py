import requests
import json
from flask import Flask, request, jsonify
#from minio import Minio
from wes_client import util
from wes_client.util import modify_jsonyaml_paths

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

    #Fix key naming for request
    param["workflow_params"] = param.pop("workflow_params/json_path")
    param["workflow_url"] = param.pop("workflow_url/name")
    #Split the comma seperated attachments into a list for input 
    param["workflow_attachment"] = param["workflow_attachment"].split(',')

    #This is the line that client uses to contruct a json object representing the parameters
    #But this gives drive specific paths
    param["workflow_params"] = modify_jsonyaml_paths(param["workflow_params"])

    clientObject = util.WESClient({'auth': '', 'proto': 'http', 'host': "wes:8080"})
    req = clientObject.run(param["workflow_url"], param["workflow_params"], param["workflow_attachment"])

    return "Workflow Request Sent"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
# TODO: ue python to run bcftools norm in process
# TODO: Generalize input workflow further
