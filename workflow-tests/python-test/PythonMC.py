# Trying to use default docker image to run a python script which downloads and configures mc, then run mc cp
# Yes, this is a strange and desperate idea
import os
os.system("mc config host add minio http://127.0.0.1:9000 miniotest miniotest --api S3v4")
os.system("mc cp minio/samples/unprocessed/NA18537.vcf.gz .")