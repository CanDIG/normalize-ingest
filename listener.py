#!/usr/bin/env python
"""
doc
"""
import json
import os
import subprocess

from flask import Flask, jsonify, request

from minio import Minio
from minio.error import ResponseError

# from wes_client import util
# from wes_client.util import modify_jsonyaml_paths


APP = Flask(__name__)
@APP.route('/events', methods=['POST'])
def main():
    """
    doc
    """
    # minio events result in two calls, so we ignore the first
    if not request.data:
        return "First Request Ignored", 406

    # Get the name of the added file
    dataobject = json.loads(request.data)['Key']
    path = dataobject.split("/")

    client = Minio('minio:9000',
                   access_key=str(os.environ["MINIO_ACCESS_KEY"]),
                   secret_key=str(os.environ["MINIO_SECRET_KEY"]),
                   secure=False)

    # Get a full object
    try:
        client.fget_object(
            str(path[0]), str(path[1] + "/" + path[2]), str(path[2]))
    except ResponseError as err:
        print(err)

    # Run bcftools via subprocess and output to local directory
    outfile = str(path[2]).split(".")
    outfile = str(outfile[0] + "-normalized.vcf")

    subprocess.run(['bcftools', 'norm', '-d', 'all', str(path[2]),
                    '-o', str(outfile)],check=True,
                   stdout=subprocess.PIPE, universal_newlines=True)

    # Put 'NA18537-normalized.vcf' into minio/samples/processed/
    try:
        client.fput_object(str(path[0]), str("processed/" + outfile),
                           str(outfile))
    except ResponseError as err:
        print(err)

    return "Workflow successful"


    # Retrieve Workflow Data from workflowInput.json
    # inFile = open("workflowInput.json", "r")
    # if inFile.mode == "r":
        # param = inFile.read()
    # param = json.loads(param)

    # Fix key naming for request
    # param["workflow_params"] = param.pop("workflow_params/json_path")
    # param["workflow_url"] = param.pop("workflow_url/name")
    # Split the comma seperated attachments into a list for input
    # param["workflow_attachment"] = param["workflow_attachment"].split(',')

    # construct a json object representing the parameters
    # But this gives drive specific paths
    # param["workflow_params"] = modify_jsonyaml_paths(param["workflow_params"])

    # clientObject = util.WESClient(
    # {'auth': '', 'proto': 'http', 'host': "wes-server:5000"})
    # req = clientObject.run(
    # param["workflow_url"], param["workflow_params"], param["workflow_attachment"])

    # return "Workflow Request Sent"


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080)
# TODO: ue python to run bcftools norm in process
# TODO: Generalize input workflow further
