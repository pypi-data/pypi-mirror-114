import json
import boto3

from typing import Dict

CLIENT = boto3.client('secretsmanager')

def get_secret(secret_name) -> Dict:
    response = CLIENT.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])
    return secret