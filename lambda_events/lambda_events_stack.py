from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_events_targets as targets,
    aws_events as events,
)
import aws_cdk as cdk
from constructs import Construct
from cdk_aws_lambda_powertools_layer import LambdaPowertoolsLayer


class LambdaEventsStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, domain_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        domain_name = domain_name

        # Defin the AWS LambdaPowertools Layer once so we can resue it
        power_tools_layer = LambdaPowertoolsLayer(self, "LambdaPowertoolsLayer")

        # An event producing lambda
        event_producer = _lambda.Function(
            self,
            "EventProducer",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_producer.handler",
            code=_lambda.Code.from_asset("lambda_producer"),
            environment={"DOMAIN_NAME": domain_name},
            layers=[power_tools_layer],
            tracing=_lambda.Tracing.ACTIVE,
        )

        # Allow the lambda to put events on the default event bus
        event_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=[f"arn:aws:events:{self.region}:{self.account}:event-bus/default"],
            actions=["events:PutEvents"],
        )
        event_producer.add_to_role_policy(event_policy)

        # An event consuming lambda
        event_consumer = _lambda.Function(
            self,
            "EventConsumer",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="lambda_consumer.handler",
            code=_lambda.Code.from_asset("lambda_consumer"),
            layers=[power_tools_layer],
            tracing=_lambda.Tracing.ACTIVE,
        )

        event_consumer_rule = events.Rule(
            self,
            "EventConsumerRole",
            description="Approved Transactions",
            event_pattern=events.EventPattern(source=[domain_name]),
        )

        event_consumer_rule.add_target(targets.LambdaFunction(handler=event_consumer))
