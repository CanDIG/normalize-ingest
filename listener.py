#!/usr/bin/env python
"""
doc
"""
import json
import os
import subprocess
import datetime

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

    # Retrieve Workflow Data from workflowInput.json
    inFile = open("workflowInput.json", "r")
    if inFile.mode == "r":
        param = inFile.read()
    param = json.loads(param)

    # Split the comma seperated attachments into a list for input
    param["workflow_attachment"] = param["workflow_attachment"].split(',')

    # Create a dictionary representing the job file
    dic = {}
    # Get the input minio url
    path = json.loads(request.data)['Key']
    dic["in-url"] = "minio/" + path

    # Get relevant data passed to the listener from the .env through env vars
    dic["out-url"] = "minio/" + os.environ["MINIO_PROCESSED_DIR"]
    dic["minio-access"] = os.environ["MINIO_ACCESS_KEY"]
    dic["minio-secret"] = os.environ["MINIO_SECRET_KEY"]
    dic["minio-domain"] = os.environ["MINIO_DOMAIN"]
    dic["minio-ui-port"] = os.environ["MINIO_UI_PORT"]

    # Add drs data and url
    d = datetime.datetime.utcnow()

    # Create the drs ingestion endpoint for the post request in the cwl
    dic["in-drs-url"] = "http://" + os.environ["DOS_HOST"] + \
        ":" + os.environ["DOS_PORT"] + "/ingest"

    # 'path' paramater in 'dataDic' needs to be the location of the file and must be accessible by the DRS container, this is currently done thorugh the named volume 'minio-data'
    # It is assumed that the input is a .'ext'.gz file, if not alter the fileExt formula
    # It is also assumed that parent folder/bucket names do not have a .
    fileExt = path[path.find("."):path.rfind(".")]
    fileName = path[path.rfind('/')+1:path.find('.')]

    # Create meta-data, this will need to conform with the metadata of the normalized object
    dataDic = {"path": os.environ["MINIO_DATA_DIR"] + "/" + os.environ["MINIO_PROCESSED_DIR"] + "/" + fileName + "-normalized" + fileExt,
               "data_object":
               {"id": "hg38-chr22",
                "name": "Human Reference Chromosome 22",
                "created": d.isoformat("T") + "Z",
                "checksums": [{"checksum": "41b47ce1cc21b558409c19b892e1c0d1", "type": "md5"}],
                "urls": [{"url": "http://hgdownload.cse.ucsc.edu/goldenPath/hg38/chromosomes/chr22.fa.gz"}],
                "size": "12255678"}}

    # Give data as string for convienence
    dic["in-drs-data"] = json.dumps(dataDic)
    job = json.dumps(dic)

    # Make request to wes
    wesLoc = "wes-server:" + os.environ["WES_PORT"]
    clientObject = util.WESClient(
        {'auth': '', 'proto': 'http', 'host': wesLoc})
    req = clientObject.run(
        param["workflow_url"], job, param["workflow_attachment"])

    return "Workflow Request Sent", 200


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=os.environ["LISTENER_PORT"])
