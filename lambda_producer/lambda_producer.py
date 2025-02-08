import json
import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info(event)
    eventbridge_client = boto3.client("events")
    request_body = event.get("body")
    logger.info(f"Raw event: {json.dumps(event)}")
    logger.info(f"Request body: {request_body}")

    if request_body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request"}),
        }

    event_bridge_event = {
        "Source": os.environ.get("DOMAIN_NAME", "example.com"),
        "DetailType": "myDetailType",
        "Detail": json.dumps({"key1": "value1", "key2": "value2"}),
        "EventBusName": "default",
    }

    logger.info(f"event_bridge_event: {event_bridge_event}")
    response = eventbridge_client.put_events(Entries=[event_bridge_event])
    logger.info(f"eventbridge_client response: {response}")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from Lambda!"}),
    }
