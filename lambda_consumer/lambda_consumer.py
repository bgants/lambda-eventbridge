from aws_lambda_powertools import Logger


logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    logger.info(event)
    request_body = event.get("body")
    logger.info(request_body)

    return {"statusCode": 200, "body": "Consumed from Lambda!"}
