import boto3

import os
import toml
from datetime import datetime


with open('.streamlit/secrets.toml', 'r') as f:
    secrets = toml.load(f)

# aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_access_key_id = secrets['AWS_ACCESS_KEY_ID']
# aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_secret_access_key = secrets['AWS_SECRET_ACCESS_KEY']
# region_name = os.getenv('AWS_DEFAULT_REGION')
region_name = secrets['AWS_DEFAULT_REGION']


dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)


table = dynamodb.Table('micronarrative_bot')


def create_entry(chat_id, prolific_id):
    '''Initialize a new entry in the table'''
    table.put_item(
        Item={
            'chat_id': chat_id, # primary key, <prolific id>-<timestamp of start>
            'prolific_id': prolific_id,  # prolific id
            'created_timestamp': datetime.now().isoformat(),  # timestamp of creation
            'interview_chat': [], # list of chat messages e.g. [{'role': 'assistant', 'content': 'hello'}, {'role': 'user', 'content': 'hi'}]
            'conversation_state': '', # phase of streamlit conversation (can help identify early termination of exercise)
            'scenario_1': '',  # AI generated scenario 1 text
            'scenario_2': '',  # AI generated scenario 2 text
            'scenario_3': '',  # AI generated scenario 3 text
            'thumb_1': '',  # either "up" or "down"
            'thumb_1_text': '',  # optional text for why the user liked or disliked the scenario
            'thumb_2': '',  # either "up" or "down"
            'thumb_2_text': '',  # optional text for why the user liked or disliked the scenario
            'thumb_3': '',  # either "up" or "down"
            'thumb_3_text': '',  # optional text for why the user liked or disliked the scenario
            'scenario_rating': '', # 1-5, rating of chosen scenario
            'scenario_choice': '',  # 1, 2, or 3
            'editing_chat': [], # [{"user_comment": "sounds too emotional", "adapted_scenario": "", "user_response": "all-good or keep-editing"}]
            'final_scenario': ''  # the final scenario that the user has approved
        }
    )

def get_entry(chat_id):
    '''Get an entry from the table'''
    response = table.get_item(
        Key={
            'chat_id': str(chat_id)
        }
    )
    item = response['Item']
    return item

def update_db_entry(chat_id, key, value):
    '''Update an entry in the table, allowing for various data types (e.g., dict, list, etc.)'''
    table.update_item(
        Key={
            'chat_id': str(chat_id)
        },
        UpdateExpression=f"set {key} = :val",
        ExpressionAttributeValues={
            ':val': value
        },
        ReturnValues="UPDATED_NEW"
    )

def append_list_entry(chat_id, key, value):
    '''Append a value to a list entry in the table'''
    table.update_item(
        Key={
            'chat_id': str(chat_id)
        },
        UpdateExpression=f"set {key} = list_append({key}, :val)",
        ExpressionAttributeValues={
            ':val': [value]
        },
        ReturnValues="UPDATED_NEW"
    )