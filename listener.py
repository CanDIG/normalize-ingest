#!/usr/bin/env python
"""
doc
"""
import json
import os
import subprocess

from flask import Flask, jsonify, request

# from minio import Minio
# from minio.error import ResponseError

from wes_client import util
from wes_client.util import modify_jsonyaml_paths

APP = Flask(__name__)
@APP.route('/events', methods=['POST'])
def main():
    """
    doc
    """
    # minio events result in two calls, so we ignore the first
    if not request.data:
        return "First Request Ignored", 406

    # # Get the name of the added file
    # dataobject = json.loads(request.data)['Key']
    # path = dataobject.split("/")

    # client = Minio('minio:9000',
    #                access_key=str(os.environ["MINIO_ACCESS_KEY"]),
    #                secret_key=str(os.environ["MINIO_SECRET_KEY"]),
    #                secure=False)

    # # Get a full object
    # try:
    #     client.fget_object(
    #         str(path[0]), str(path[1] + "/" + path[2]), str(path[2]))
    # except ResponseError as err:
    #     print(err)

    # # Run bcftools via subprocess and output to local directory
    # outfile = str(path[2]).split(".")
    # outfile = str(outfile[0] + "-normalized.vcf")

    # subprocess.run(['bcftools', 'norm', '-d', 'all', str(path[2]),
    #                 '-o', str(outfile)],check=True,
    #                stdout=subprocess.PIPE, universal_newlines=True)

    # # Put 'NA18537-normalized.vcf' into minio/samples/processed/
    # try:
    #     client.fput_object(str(path[0]), str("processed/" + outfile),
    #                        str(outfile))
    # except ResponseError as err:
    #     print(err)

    # return "Workflow successful"

    # Retrieve Workflow Data from workflowInput.json
    inFile = open("workflowInput.json", "r")
    if inFile.mode == "r":
        param = inFile.read()
    param = json.loads(param)

    # Split the comma seperated attachments into a list for input
    param["workflow_attachment"] = param["workflow_attachment"].split(',')

    # Create a dictionary representing the job file
    dic = {}
    # get the input minio url
    path = json.loads(request.data)['Key']
    dic["in-url"] = "minio/" + path

    dic["out-url"] = "minio/samples/processed" # This will probably be set to somewhere fixed
    dic["minio-access"] = os.environ["MINIO_ACCESS_KEY"]
    dic["minio-secret"] = os.environ["MINIO_SECRET_KEY"]
    dic["minio-domain"] = os.environ["MINIO_DOMAIN"]
    dic["minio-ui-port"] = os.environ["MINIO_UI_PORT"]

    # Add drs data and url
    dic["in-drs-url"] = "http://" + os.environ["DOS_HOST"] + \
        ":" + os.environ["DOS_PORT"] + "/ga4gh/dos/v1/dataobjects"
    dataDic = {"data_object":
               {"id": "hg38-chr22",
                "name": "Human Reference Chromosome 22",
                "checksums": [{"checksum": "41b47ce1cc21b558409c19b892e1c0d1", "type": "md5"}],
                "urls": [{"url": "http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz"}],
                "size": "12255678"}}
    dic["in-drs-data"] = json.dumps(dataDic) # Give data as string for convienence

    job = json.dumps(dic)

    wesLoc = "wes-server:" + os.environ["WES_PORT"]
    clientObject = util.WESClient(
        {'auth': '', 'proto': 'http', 'host': wesLoc})
    req = clientObject.run(
        param["workflow_url"], job, param["workflow_attachment"])

    return "Workflow Request Sent", 200


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8081)
# TODO: ue python to run bcftools norm in process
# TODO: Generalize input workflow further
