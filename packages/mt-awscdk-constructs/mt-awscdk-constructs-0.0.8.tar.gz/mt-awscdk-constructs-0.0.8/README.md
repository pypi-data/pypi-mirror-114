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
