import boto3
from botocore.exceptions import ClientError

def validate_bedrock_model(model_id):
    try:
        client = boto3.client('bedrock')
        response = client.get_foundation_model(
            modelIdentifier=model_id
        )
        return True
    except ClientError:
        return False
