import boto3
import json
import uuid
import time

# Make our dynamodb connection
dynamo = boto3.client("dynamodb", "us-east-1")


# Transform the data from sqs and send to dynamodb
def lambda_handler(event, context):
    """
    Obtains data from the SQS message, adds a uuid to each record, transforms the data to the proper DynamoDB format and sends the data to the DynamoDB table.
    :param event: SQS Message
    :param context: None
    :return: None
    """
    for item in json.loads(event["Records"][0]["body"]):
        item["id"] = uuid.uuid1().bytes
        for key, value in item.items():
            if key == "id":
                item[key] = {"B": bytes(value)}
            elif key == "fiscal_year":
                item[key] = {"N": str(value)}
            elif key == "emissions_mtco2e":
                item[key] = {"N": str(value)}
            elif key == "consumption":
                item[key] = {"N": str(value)}
            else:
                item[key] = {"S": str(value)}

            time.sleep(0.001)

        dynamo.put_item(TableName="Greenhouse_gas_emissions", Item=dict(item))
