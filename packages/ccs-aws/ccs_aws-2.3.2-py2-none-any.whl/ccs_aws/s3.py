import json
import gzip
import io
from datetime import datetime
import boto3 
from typing import List, Dict

CLIENT = boto3.client('s3')

def upload_compressed_data(bucket: str, key: str, record_list: List[Dict], default=None, encoding='utf-8'):
    ''' upload python dict into s3 bucket with gzip archive '''
    inmem = io.BytesIO()
    with gzip.GzipFile(fileobj=inmem, mode='wb') as fh:
        with io.TextIOWrapper(fh, encoding=encoding) as wrapper:
            for record in record_list:
                wrapper.write(f'{json.dumps(record, ensure_ascii=False, default=default)}\n')
    inmem.seek(0)
    CLIENT.put_object(Bucket=bucket, Body=inmem, Key=key)

def download_json_gz(bucket: str, key: str):
    ''' download gzipped json file from s3 and convert to dict '''
    response = CLIENT.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read()
    with gzip.GzipFile(fileobj=io.BytesIO(content), mode='rb') as fh:
        return json.load(fh)

def upload_data(bucket: str, key: str, file_obj):
    CLIENT.put_object(Bucket=bucket, Body=json.dumps(file_obj), Key=key)