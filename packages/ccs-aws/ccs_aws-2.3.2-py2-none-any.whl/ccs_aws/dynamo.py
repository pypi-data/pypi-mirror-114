import json
from datetime import datetime
import boto3 
from typing import List, Dict
from boto3.dynamodb.conditions import Key

CLIENT = boto3.client('dynamodb')

TYPE_MAP = [
    {
        "python_types": [str],
        "dynamo_type": 'S'
    },
    {
        "python_types": [int, float],
        "dynamo_type": 'N'
    },
    {
        "python_types": [bytes],
        "dynamo_type": 'BS'
    },
    {
        "python_types": [None],
        "dynamo_type": 'NULL'
    },
    {
        "python_types": [bool],
        "dynamo_type": 'BOOL'
    }
]

def query_by_vendor(table: str, vendor: str) -> List[dict]: 
    response = CLIENT.query(
        TableName=table,
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression='vendor = :vendor',
        ExpressionAttributeValues={
            ':vendor': {'S': vendor}
        }
    )
    return response['Items']

def query_by_sku(table: str, vendor: str, sku: str) -> List[dict]:
    response = CLIENT.query(
        TableName=table,
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression='vendor = :vendor and sku = :sku',
        ExpressionAttributeValues={
            ':vendor': {'S': vendor.strip()},
            ':sku': {'S': sku.strip()}
        }
    )
    items = response['Items']
    if len(items) > 1:
        raise ValueError("This query should contain a maximum of 1 result. More than one result returned.")
    order_data = {}
    for data_key, data_value in items[0].items():
        for item_key, item_value in data_value.items():
            order_data.update({data_key: item_value})
    return order_data

def query_item(table: str, vendor: str) -> List[dict]:
    response = CLIENT.query(
        TableName=table,
        Select='ALL_ATTRIBUTES',
        KeyConditionExpression='vendor = :vendor',
    )

def update_stock(table: str, item: Dict):
    response = CLIENT.update_item(
        TableName=table,
        Key={
            'vendor': item['vendor'],
            'sku': item['sku']
        },
        UpdateExpression='set currently_out_of_stock=:currently_out_of_stock',
        ExpressionAttributeValues={
            ':currently_out_of_stock': item['currently_out_of_stock']
        }
    )
    return response

def upload(json_data: json):
    for item in json_data:
        upload_item = {
            'sku': {'S': item['sku'].lower().strip()},
            'vendor': {'S': item['vendor'].lower().strip()},
            'name': {'S': item['name'].lower().strip()},
            'url': {'S': item['url'].lower().strip()},
            'css_selector_class': {'S': item['css_selector_class'].strip()},
            'out_of_stock_text': {'S': item['out_of_stock_text'].lower().strip()},
            'currently_out_of_stock': {'BOOL': item['currently_out_of_stock']}
        }
        print(upload_item)
        response = CLIENT.put_item(
            TableName='DropshipItems',
            Item=upload_item
        )
        print('UPLOADING ITEM')
        print(response)
