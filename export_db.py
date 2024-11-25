import boto3
import os
from decimal import Decimal
from dotenv import load_dotenv
import json
from boto3.dynamodb.conditions import Key
import pandas as pd

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

def export_dynamodb_to_json(table_name, output_file, consistent_read=False):
    # Initialize DynamoDB client
    table = dynamodb.Table(table_name)
    
    # Scan the entire table
    response = table.scan()
    data = response['Items']
    
    # Keep scanning until all items are retrieved
    while 'LastEvaluatedKey' in response:
        print("Fetching more data...")
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'], ConsistentRead=consistent_read)
        data.extend(response['Items'])
    
    # Save to JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, cls=DecimalEncoder, indent=4)
    
    print(f"Data exported to {output_file} successfully.")
    
def dynamodb_to_csv_1(pt1_json_dict, output_dir):
    scenario_csv_list = []
    for item in pt1_json_dict:
        row = {
            'pid': item['chat_id'],
            'timestamp': item['timestamp'],
            'scenario': item['scenario'],
            'answer_set_context': item['answer set']['context'],
            'answer_set_what': item['answer set']['what'],
            'answer_set_reaction': item['answer set']['reaction'],
            'answer_set_outcome': item['answer set']['outcome'],
            
        }
        scenario_csv_list.append(row)
    df_scenario = pd.DataFrame(scenario_csv_list)
    
    proposed_scenarios_csv_list = []
    score1, text1, score2, text2, score3, text3 = '', '', '', '', '', ''
    for item in pt1_json_dict:
        if item['scenarios_all']['fb1'] and item['scenarios_all']['fb1'] != '':
            score1 = item['scenarios_all']['fb1']['score']
            text1 = item['scenarios_all']['fb1']['text']
        if item['scenarios_all']['fb2'] and item['scenarios_all']['fb2'] != '':
            score2 = item['scenarios_all']['fb2']['score']
            text2 = item['scenarios_all']['fb2']['text']
        if item['scenarios_all']['fb3'] and item['scenarios_all']['fb3'] != '':
            score3 = item['scenarios_all']['fb3']['score']
            text3 = item['scenarios_all']['fb3']['text']
        row = {
            'pid': item['chat_id'],
            'timestamp': item['timestamp'],
            'proposed_scenario_1': item['scenarios_all']['col1'],
            'proposed_scenario_1_score': score1,
            'proposed_scenario_1_text': text1,
            'proposed_scenario_2': item['scenarios_all']['col2'],
            'proposed_scenario_2_score': score2,
            'proposed_scenario_2_text': text2,
            'proposed_scenario_3': item['scenarios_all']['col3'],
            'proposed_scenario_3_score': score3,
            'proposed_scenario_3_text': text3
        }
        proposed_scenarios_csv_list.append(row)
    df_proposed_scenarios = pd.DataFrame(proposed_scenarios_csv_list)
    
    interview_chat_csv_list = []
    for item in pt1_json_dict:
        chat_history = item['chat_history']
        for chat in chat_history:
            row = {
                'pid': item['chat_id'],
                'timestamp': item['timestamp'],
                'role': chat[0],
                'content': chat[1]
            }
            interview_chat_csv_list.append(row)
    df_interview_chat = pd.DataFrame(interview_chat_csv_list)
            
    adaptation_chat_csv_list = []
    for item in pt1_json_dict:
        chat_history = item['adaptation_list']
        if chat_history:
            chat_history = chat_history[0]
            for chat in chat_history:
                row = {
                    'pid': item['chat_id'],
                    'timestamp': item['timestamp'],
                    'content': chat
                }
                adaptation_chat_csv_list.append(row)

    df_adaptation_chat = pd.DataFrame(adaptation_chat_csv_list)
    
    df_scenario.to_csv(os.path.join(output_dir, 'final_scenarios_pt1.csv'), index=False)
    df_proposed_scenarios.to_csv(os.path.join(output_dir, 'proposed_scenarios_pt1.csv'), index=False)
    df_interview_chat.to_csv(os.path.join(output_dir, 'interview_chat_pt1.csv'), index=False)
    df_adaptation_chat.to_csv(os.path.join(output_dir, 'adaptation_chat_pt1.csv'), index=False)

def dynamodb_to_csv_2(pt2_json_dict, output_dir):
    
    scenario_csv_list = []
    for item in pt2_json_dict:
        if 'study_code' in item:
           study_code = item['study_code']
        else:
            study_code = '' 
        row = {
            'pid': item['chat_id'],
            'timestamp': item['timestamp'],
            'study_code': study_code,
            'scenario': item['scenario'],
            'answer_set_perspective': item['answer set']['perspective'],
            'answer_set_recommendation': item['answer set']['recommendation'],
            'answer_set_reaction': item['answer set']['reaction'],
            'answer_set_desired': item['answer set']['desiredreaction'],
            
        }
        scenario_csv_list.append(row)
    df_scenario = pd.DataFrame(scenario_csv_list)
    
    proposed_scenarios_csv_list = []
    for item in pt2_json_dict:
        score1, text1, score2, text2, score3, text3 = '', '', '', '', '', ''
        if item['scenarios_all']['fb1'] and item['scenarios_all']['fb1'] != '':
            score1 = item['scenarios_all']['fb1']['score']
            text1 = item['scenarios_all']['fb1']['text']
        if item['scenarios_all']['fb2'] and item['scenarios_all']['fb2'] != '':
            score2 = item['scenarios_all']['fb2']['score']
            text2 = item['scenarios_all']['fb2']['text']
        if item['scenarios_all']['fb3'] and item['scenarios_all']['fb3'] != '':
            score3 = item['scenarios_all']['fb3']['score']
            text3 = item['scenarios_all']['fb3']['text']
        row = {
            'pid': item['chat_id'],
            'timestamp': item['timestamp'],
            'proposed_scenario_1': item['scenarios_all']['col1'],
            'proposed_scenario_1_score': score1,
            'proposed_scenario_1_text': text1,
            'proposed_scenario_2': item['scenarios_all']['col2'],
            'proposed_scenario_2_score': score2,
            'proposed_scenario_2_text': text2,
            'proposed_scenario_3': item['scenarios_all']['col3'],
            'proposed_scenario_3_score': score3,
            'proposed_scenario_3_text': text3
        }
        proposed_scenarios_csv_list.append(row)
    df_proposed_scenarios = pd.DataFrame(proposed_scenarios_csv_list)
    
    interview_chat_csv_list = []
    for item in pt2_json_dict:
        chat_history = item['chat_history']
        for chat in chat_history:
            row = {
                'pid': item['chat_id'],
                'timestamp': item['timestamp'],
                'role': chat[0],
                'content': chat[1]
            }
            interview_chat_csv_list.append(row)
    df_interview_chat = pd.DataFrame(interview_chat_csv_list)
    
    df_scenario.to_csv(os.path.join(output_dir, 'final_scenarios_pt2.csv'), index=False)
    df_proposed_scenarios.to_csv(os.path.join(output_dir, 'proposed_scenarios_pt2.csv'), index=False)
    df_interview_chat.to_csv(os.path.join(output_dir, 'interview_chat_pt2.csv'), index=False)
    


if __name__ == '__main__':
    
    DYNAMODB_TABLE_NAME_1 = 'petr_micronarrative_nov2024'
    OUTPUT_FILE_1 = 'petr_micronarrative_nov2024_pt1.json'
    export_dynamodb_to_json(DYNAMODB_TABLE_NAME_1, OUTPUT_FILE_1)
    
    with open(OUTPUT_FILE_1, 'r') as f:
        pt1_json_dict = json.load(f)
    dynamodb_to_csv_1(pt1_json_dict, '')
    
    
    DYNAMODB_TABLE_NAME_2 = 'petr_micronarrative_nov2024_2'
    OUTPUT_FILE_2 = 'petr_micronarrative_nov2024_pt2.json'
    export_dynamodb_to_json(DYNAMODB_TABLE_NAME_2, OUTPUT_FILE_2)
    
    with open(OUTPUT_FILE_2, 'r') as f:
        pt2_json_dict = json.load(f)
        
    dynamodb_to_csv_2(pt2_json_dict, '')
    
    