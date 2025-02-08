#!/usr/bin/env python3
import os

import aws_cdk as cdk

from lambda_events.lambda_events_stack import LambdaEventsStack


account = os.getenv("AWS_ACCOUNT_ID")
primary_region = os.getenv("AWS_PRIMARY_REGION")
domain_name = os.getenv("AWS_DOMAIN_NAME")
primary_environment = cdk.Environment(account=account, region=primary_region)

app = cdk.App()
LambdaEventsStack(
    app, "LambdaEventsStack", env=primary_environment, domain_name=domain_name
)
app.synth()
