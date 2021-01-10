import pytest
from pytest import ExitCode
import boto3
from boto3.dynamodb.conditions import Key

dynamo = boto3.resource("dynamodb", "us-east-1")
table = dynamo.Table("Greenhouse_gas_emissions")


def check_num_records():
    """
    Checks the number of records in the DynamoDB table
    :return: True if the item count is equal to 345442
    """
    assert table.item_count == 345442


def check_record_format():
    """
    Checks the format of records in the DynamoDB Table
    :return: True if the DynamoDB record has the listed keys
    """
    keys = [
        "fiscal_year",
        "department",
        "consumption_units",
        "emissions_mtco2e",
        "consumption",
        "source_type",
        "id",
        "quarter",
    ]

    scan_kwargs = {"FilterExpression": Key("consumption").gte(0)}

    data = table.scan(**scan_kwargs)["Items"][0]

    lst = []

    for i in data.keys():
        lst.append(i)

    assert keys == lst
