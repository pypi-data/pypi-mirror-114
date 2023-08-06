'''
# Marley Tech AWS CDK Construct Library

A collection of useful AWS CDK Constructs.

## Constructs

### EventFunction

A Construct which provides the resource for triggering a Lambda Function via a EventBridge Rule. It includes the Dead Letter Queues for the delivery and the processing of the event.

![Event Function Architecture Diagram](docs/EventFunction/EventFunction.png)

The Event Function Lambda is given the following Environment Variables:

* `PROCESSING_DLQ_ARN` - the SQS Queue ARN of the Processing DLQ (to assist the Lambda Code to publish failed messages to this queue)
* `PROCESSING_DLQ_NAME` - the SQS Queue Name of the Processing DLQ (to assist the Lambda Code to publish failed messages to this queue)

#### Resources

This Construct deploy the following resources:

* Rule (EventBridge Rule) - The trigger or event rule which will be passed to the Event Function
* Event Function (Lambda Function) - The code which will be executed
* Delivery DLQ (SQS Queue) - A DLQ which undeliverable Events are pushed to (e.g. if the Event Function is unreachable)
* Processing DLQ (SQS Queue) - A DLQ which the Event Fucntion may push Events to if it considers the Event to be unprocessable (e.g. if the Event is in an unexpected structure)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Contributor Code Of Conduct

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree
to abide [by its terms](CODE_OF_CONDUCT.md).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_events
import aws_cdk.aws_lambda
import aws_cdk.aws_sqs
import aws_cdk.core


class EventFunction(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="mt-awscdk-constructs.EventFunction",
):
    '''EventFunction.

    A Lambda Function, triggered by an EventBridge Event

    Includes additional resources:

    - Configurable EventBridge Rule
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: "IEventFunctionProps",
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(EventFunction, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryDlq")
    def delivery_dlq(self) -> aws_cdk.aws_sqs.IQueue:
        '''The SQS Queue which acts as a DLQ for any EventBridge Delivery failures.'''
        return typing.cast(aws_cdk.aws_sqs.IQueue, jsii.get(self, "deliveryDlq"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> aws_cdk.aws_lambda.IFunction:
        '''Lambda Function which is the target of the Event.'''
        return typing.cast(aws_cdk.aws_lambda.IFunction, jsii.get(self, "lambdaFunction"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="processingDlq")
    def processing_dlq(self) -> aws_cdk.aws_sqs.IQueue:
        '''The SQS Queue which acts as a DLQ for any events which the Event Function is unable to process.'''
        return typing.cast(aws_cdk.aws_sqs.IQueue, jsii.get(self, "processingDlq"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="rule")
    def rule(self) -> aws_cdk.aws_events.IRule:
        '''EventBridge Rule which controls when the Event Function is triggered.'''
        return typing.cast(aws_cdk.aws_events.IRule, jsii.get(self, "rule"))


@jsii.interface(jsii_type="mt-awscdk-constructs.IEventFunctionDeliveryProps")
class IEventFunctionDeliveryProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxEventAge")
    def max_event_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.'''
        ...

    @max_event_age.setter
    def max_event_age(self, value: typing.Optional[aws_cdk.core.Duration]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.'''
        ...

    @retry_attempts.setter
    def retry_attempts(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _IEventFunctionDeliveryPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "mt-awscdk-constructs.IEventFunctionDeliveryProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="maxEventAge")
    def max_event_age(self) -> typing.Optional[aws_cdk.core.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.'''
        return typing.cast(typing.Optional[aws_cdk.core.Duration], jsii.get(self, "maxEventAge"))

    @max_event_age.setter
    def max_event_age(self, value: typing.Optional[aws_cdk.core.Duration]) -> None:
        jsii.set(self, "maxEventAge", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttempts"))

    @retry_attempts.setter
    def retry_attempts(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "retryAttempts", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEventFunctionDeliveryProps).__jsii_proxy_class__ = lambda : _IEventFunctionDeliveryPropsProxy


@jsii.interface(jsii_type="mt-awscdk-constructs.IEventFunctionProps")
class IEventFunctionProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionProps")
    def function_props(self) -> aws_cdk.aws_lambda.FunctionProps:
        '''Configuration of the Event Function Lambda.

        :readonly: true
        '''
        ...

    @function_props.setter
    def function_props(self, value: aws_cdk.aws_lambda.FunctionProps) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleProps")
    def rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''The configuration and behaviour of the EventBridge Rule which links the EventBus and the Event Function Lambda.

        :readonly: true
        '''
        ...

    @rule_props.setter
    def rule_props(self, value: aws_cdk.aws_events.RuleProps) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryDlqProps")
    def delivery_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Delivery DLQ.

        :readonly: true
        '''
        ...

    @delivery_dlq_props.setter
    def delivery_dlq_props(
        self,
        value: typing.Optional[aws_cdk.aws_sqs.QueueProps],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryProps")
    def delivery_props(self) -> typing.Optional[IEventFunctionDeliveryProps]:
        '''Configuration of the Delivery properties to the Event Function Lambda.

        :readonly: true
        '''
        ...

    @delivery_props.setter
    def delivery_props(
        self,
        value: typing.Optional[IEventFunctionDeliveryProps],
    ) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="processingDlqProps")
    def processing_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Processing DLQ.

        :readonly: true
        '''
        ...

    @processing_dlq_props.setter
    def processing_dlq_props(
        self,
        value: typing.Optional[aws_cdk.aws_sqs.QueueProps],
    ) -> None:
        ...


class _IEventFunctionPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "mt-awscdk-constructs.IEventFunctionProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="functionProps")
    def function_props(self) -> aws_cdk.aws_lambda.FunctionProps:
        '''Configuration of the Event Function Lambda.

        :readonly: true
        '''
        return typing.cast(aws_cdk.aws_lambda.FunctionProps, jsii.get(self, "functionProps"))

    @function_props.setter
    def function_props(self, value: aws_cdk.aws_lambda.FunctionProps) -> None:
        jsii.set(self, "functionProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ruleProps")
    def rule_props(self) -> aws_cdk.aws_events.RuleProps:
        '''The configuration and behaviour of the EventBridge Rule which links the EventBus and the Event Function Lambda.

        :readonly: true
        '''
        return typing.cast(aws_cdk.aws_events.RuleProps, jsii.get(self, "ruleProps"))

    @rule_props.setter
    def rule_props(self, value: aws_cdk.aws_events.RuleProps) -> None:
        jsii.set(self, "ruleProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryDlqProps")
    def delivery_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Delivery DLQ.

        :readonly: true
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], jsii.get(self, "deliveryDlqProps"))

    @delivery_dlq_props.setter
    def delivery_dlq_props(
        self,
        value: typing.Optional[aws_cdk.aws_sqs.QueueProps],
    ) -> None:
        jsii.set(self, "deliveryDlqProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="deliveryProps")
    def delivery_props(self) -> typing.Optional[IEventFunctionDeliveryProps]:
        '''Configuration of the Delivery properties to the Event Function Lambda.

        :readonly: true
        '''
        return typing.cast(typing.Optional[IEventFunctionDeliveryProps], jsii.get(self, "deliveryProps"))

    @delivery_props.setter
    def delivery_props(
        self,
        value: typing.Optional[IEventFunctionDeliveryProps],
    ) -> None:
        jsii.set(self, "deliveryProps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="processingDlqProps")
    def processing_dlq_props(self) -> typing.Optional[aws_cdk.aws_sqs.QueueProps]:
        '''Configuration of the Processing DLQ.

        :readonly: true
        '''
        return typing.cast(typing.Optional[aws_cdk.aws_sqs.QueueProps], jsii.get(self, "processingDlqProps"))

    @processing_dlq_props.setter
    def processing_dlq_props(
        self,
        value: typing.Optional[aws_cdk.aws_sqs.QueueProps],
    ) -> None:
        jsii.set(self, "processingDlqProps", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEventFunctionProps).__jsii_proxy_class__ = lambda : _IEventFunctionPropsProxy


__all__ = [
    "EventFunction",
    "IEventFunctionDeliveryProps",
    "IEventFunctionProps",
]

publication.publish()
