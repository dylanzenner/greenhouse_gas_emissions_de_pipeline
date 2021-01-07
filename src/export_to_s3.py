import boto3

# Make our DynamoDB connection
dynamo = boto3.client("dynamodb", "us-east-1")


# Get dynamodb table ARN from SecretsManager
def get_table_arn():
    """
    Retrieves the DynamoDB table ARN from SecretsManager
    :return: Secret Table ARN
    """
    client = boto3.client("secretsmanager", "us-east-1")
    response = client.get_secret_value(SecretId="dynamodb_arn")
    return response["SecretString"]


# Export the data to S3
def lambda_handler(event, context):
    """
    Exports the data from DynamoDB to S3
    :return: None
    """
    dynamo.export_table_to_point_in_time(
        TableArn=get_table_arn(), S3Bucket="greenhouse-gas-emissions"
    )
