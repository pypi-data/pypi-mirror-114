# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import boto3
import logging
import os
try:
    import queue
except ImportError:
    import Queue as queue

import greengrasssdk
from greengrass_common.env_vars import MY_FUNCTION_ARN
from greengrass_ipc_python_sdk.ipc_client import IPCClient
from connector_lambda_python_commons import utilities

from DeepGreenFeedbackConnectorLambda.model.feedback_input import FeedbackInput
from DeepGreenFeedbackConnectorLambda.model.connector_config import (
    ConnectorConfig, PARAM_FEEDBACK_CONFIG_MAP, PARAM_MAX_REQUESTS)
from DeepGreenFeedbackConnectorLambda.request_processor import RequestProcessor
from DeepGreenFeedbackConnectorLambda.service.cloudwatch_metrics_publisher import CWConnectorMetricsPublisher
from DeepGreenFeedbackConnectorLambda.service.model_input_uploader import ModelInputUploader
from DeepGreenFeedbackConnectorLambda.service.model_prediction_publisher import ModelPredictionPublisher
from DeepGreenFeedbackConnectorLambda.service.status_publisher import StatusPublisher, StatusMessageError

COUNTER_INVALID_CONNECTOR_CONFIG = "ErrorInvalidConnectorConfig"
COUNTER_INVALID_INPUT = "ErrorInvalidInput"
COUNTER_MISSING_REQUEST_ID = "ErrorMissingRequestId"
COUNTER_REQUEST_THROTTLED = "ErrorRequestThrottled"

iot_client = greengrasssdk.client('iot-data')
model_prediction_publisher = ModelPredictionPublisher(iot_client)
status_publisher = StatusPublisher(iot_client)
metrics_publisher = CWConnectorMetricsPublisher(iot_client)
s3_client = boto3.client('s3')
model_input_uploader = ModelInputUploader(s3_client, metrics_publisher)

# Use client to tell Greengrass whether or not a deployment
# is successful. Note: For this to work properly, the
# InitializationTimeout variable must be set in the lambda
# configuration.
client = IPCClient('localhost', 8000)

try:
    # This try block is for catching user configuration errors
    connector_param_feedback_config = utilities.get_required_environment_variable(PARAM_FEEDBACK_CONFIG_MAP)
    connector_param_max_requests = os.environ.get(PARAM_MAX_REQUESTS, 0)
    connector_config = ConnectorConfig(
        int(connector_param_max_requests if connector_param_max_requests else 0),
        connector_param_feedback_config
    )
except Exception as e:
    metrics_publisher.publish_counter(COUNTER_INVALID_CONNECTOR_CONFIG, 1)
    error_str = "Failed to initialize {}. Exception raised while parsing connector configuration. Stopping connector execution. Failed with: {}".format(MY_FUNCTION_ARN, e)
    logging.error(error_str)
    client.put_initialization_result(MY_FUNCTION_ARN, error_str)
    raise e

try:
    # This try block is for catching unexpected errors
    request_queue = queue.Queue(connector_config.max_requests)
    request_processor = RequestProcessor(
        request_queue=request_queue,
        metrics_publisher=metrics_publisher,
        status_publisher=status_publisher,
        model_input_uploader=model_input_uploader,
        model_prediction_publisher=model_prediction_publisher
    )

    # request_processor runs on a separate thread and listens for
    # events published to the request_queue.
    request_processor.start()
except Exception as e:
    error_str = "Failed to initialize {}. Unexpected exception raised:{}".format(MY_FUNCTION_ARN, e)
    logging.error(error_str)
    client.put_initialization_result(MY_FUNCTION_ARN, error_str)
    raise e

logging.info("Successfuly initialized the feedback connector.")
client.put_initialization_result(MY_FUNCTION_ARN, None)


def handle_error(request_id, exception, error_str, counter):
        metrics_publisher.publish_counter(counter, 1)
        logging.warn(error_str)
        error_message = StatusMessageError(request_id=request_id, exception=exception, message=error_str)
        status_publisher.publish(error_message)


def function_handler(event, context):
    # Validate input and return to client immediately if something is
    # wrong.
    try:
        request_id = context.aws_request_id
        if not request_id:
            raise ValueError("No aws_request_id was found in input context.")
    except Exception as e:
        error_str = "Exception raised while extracting request id. Failed with exception type: {}, error: {}".format(type(e).__name__, e)
        handle_error(request_id="", exception=e, error_str=error_str, counter=COUNTER_MISSING_REQUEST_ID)
        raise e

    try:
        feedback_input = FeedbackInput(request_id, event, context.client_context.custom)
        if feedback_input.config_id not in connector_config.feedback_config_map:
            raise ValueError("Feedback configuration map does not contain config_id: {}".format(feedback_input.config_id))
        feedback_config = connector_config.feedback_config_map[feedback_input.config_id]
    except Exception as e:
        error_str = "Exception raised while parsing input. Failed with exception type: {}, error: {}".format(type(e).__name__, e)
        handle_error(request_id=request_id, exception=e, error_str=error_str, counter=COUNTER_INVALID_INPUT)
        raise e

    try:
        logging.info("Enqueing request to be processed. Request Id: {}".format(request_id))
        request_queue.put_nowait((feedback_input, feedback_config))
    except queue.Full as e:
        error_str = "Request limit has been reached (max request:{}). Dropping request.".format(connector_config.max_requests)
        handle_error(request_id=request_id, exception=e, error_str=error_str, counter=COUNTER_REQUEST_THROTTLED)
        raise e

    logging.info("Request has successfully be enqueued. Request Id: {}".format(request_id))
    return
