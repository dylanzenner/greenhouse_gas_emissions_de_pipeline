import json
import urllib3
import certifi
from sodapy import Socrata
import boto3

# Define our Pool Manager and our url connection strings
http = urllib3.PoolManager(ca_certs=certifi.where())
url = "https://data.sfgov.org/resource"
url2 = "data.sfgov.org"


# Get secret api token value
def get_secret_api_token():
    """
    Accesses AWS Secrets Manager and retrieves the secret app token for the API
    :return: secret api_token
    """
    client = boto3.client("secretsmanager", "us-east-1")
    response = client.get_secret_value(SecretId="API_Access_Token")

    secret_dict = json.loads(response["SecretString"])
    return secret_dict["api_token"]


# Get secret sqs connection string
def get_secret_sqs_connection_string():
    """
    Accesses AWS Secrets Manager and retrieves the secret sqs connection string
    :return: secret sqs connection string
    """
    client = boto3.client("secretsmanager", "us-east-1")
    response = client.get_secret_value(SecretId="sqs_queue")

    secret_dict = json.loads(response["SecretString"])
    return secret_dict["sqs"]


# Check connection to the url of the API
def check_connection():
    """
    Checks the connection status of the url
    :return: Either 'Connection Successful' or 'Connection Failed'
    """
    try:
        http.request("GET", url, retries=False)
        return "Connection Successful"
    except urllib3.exceptions.NewConnectionError:
        return "Connection Failed"


# Pull data and send to SQS Queue
def pull_socrata():
    """
    Pulls the data from the socrata API endpoint and sends it to an SQS queue
    :return: None or Connection Failed
    """
    sqs = boto3.client("sqs", "us-east-1")

    s = Socrata(url2, get_secret_api_token())

    loop_size = 1000
    num_of_loops = 346
    if check_connection() == "Connection Successful":
        for i in range(num_of_loops):
            r = s.get("pxac-sadh", limit=loop_size, offset=loop_size * i)
            data = json.dumps(r)
            sqs.send_message(
                QueueUrl=get_secret_sqs_connection_string(), MessageBody=data
            )
    else:
        return "Connection Failed"


def lambda_handler(event, context):
    """
    Calls the pull_socrata() function which pulls the data from the API in batches and sends them to an SQS Queue
    :return: None
    """
    pull_socrata()
