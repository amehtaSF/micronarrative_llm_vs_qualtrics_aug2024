import boto3
import os
from decimal import Decimal
from dotenv import load_dotenv
import json
from boto3.dynamodb.conditions import Key

load_dotenv()


aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_DEFAULT_REGION')


dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

# Custom class to handle Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def export_dynamodb_to_json(table_name, output_file):
    # Initialize DynamoDB client
    table = dynamodb.Table(table_name)
    
    # Scan the entire table
    response = table.scan()
    data = response['Items']
    
    # Keep scanning until all items are retrieved
    while 'LastEvaluatedKey' in response:
        print("Fetching more data...")
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, cls=DecimalEncoder, indent=4)
    
    print(f"Data exported to {output_file} successfully.")


if __name__ == '__main__':
    
    DYNAMODB_TABLE_NAME_1 = 'petr_micronarrative_nov2024'
    OUTPUT_FILE_1 = 'petr_micronarrative_nov2024_pt1.json'
    export_dynamodb_to_json(DYNAMODB_TABLE_NAME_1, OUTPUT_FILE_1)
    
    DYNAMODB_TABLE_NAME_2 = 'petr_micronarrative_nov2024_2'
    OUTPUT_FILE_2 = 'petr_micronarrative_nov2024_pt2.json'
    export_dynamodb_to_json(DYNAMODB_TABLE_NAME_2, OUTPUT_FILE_2)
    