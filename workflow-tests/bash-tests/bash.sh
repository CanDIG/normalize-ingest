mc config host add minio http://127.0.0.1:9000 miniotest miniotest --api S3v4
mc cp minio/samples/unprocessed/NA18537.vcf.gz .