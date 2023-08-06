# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import boto3
import logging
import os
import json

try:
    import queue
except ImportError:
    import Queue as queue

import awsiot.greengrasscoreipc


from feedbackloop.model.feedback_input import FeedbackInput
from feedbackloop.model.connector_config import (
    ConnectorConfig, PARAM_FEEDBACK_CONFIG_MAP, PARAM_MAX_REQUESTS)
from feedbackloop.simple_request_processor import SimpleRequestProcessor
from feedbackloop.service.model_input_uploader_nocw import ModelInputUploaderNoCW
from feedbackloop.service.model_prediction_publisher import ModelPredictionPublisher

COUNTER_INVALID_CONNECTOR_CONFIG = "ErrorInvalidConnectorConfig"
COUNTER_INVALID_INPUT = "ErrorInvalidInput"
COUNTER_MISSING_REQUEST_ID = "ErrorMissingRequestId"
COUNTER_REQUEST_THROTTLED = "ErrorRequestThrottled"

s3_client = boto3.client('s3')
model_input_uploader = ModelInputUploaderNoCW(s3_client)

ipc_client = awsiot.greengrasscoreipc.connect()
model_prediction_publisher = ModelPredictionPublisher(ipc_client)


try:
    # This try block is for catching user configuration errors
    # connector_param_feedback_config = utilities.get_required_environment_variable(PARAM_FEEDBACK_CONFIG_MAP)
    #f = open('feedback_config.json')
    #PARAM_FEEDBACK_CONFIG_MAP = json.dumps(json.load(f))
    PARAM_FEEDBACK_CONFIG_MAP = '''
    {
        "ConfigID1": {
            "s3-bucket-name": "my-aws-bucket-random-sampling-747745259168",
            "content-type": "text/txt",
            "file-ext": "txt",
            "sampling-strategy": {
                "strategy-name": "RANDOM_SAMPLING",
                "rate": 1.0
            }
        },
        "ConfigID2": {
            "s3-bucket-name": "my-aws-bucket-margin-sampling-747745259168",
            "content-type": "text/txt",
            "file-ext": "txt",
            "sampling-strategy": {
                "strategy-name": "MARGIN",
                "threshold": 0.2
            }
        }
    }
    '''
    connector_param_feedback_config = json.loads(PARAM_FEEDBACK_CONFIG_MAP)
    # connector_param_max_requests = os.environ.get(PARAM_MAX_REQUESTS, 0)
    connector_param_max_requests = 10
    connector_config = ConnectorConfig(
        int(connector_param_max_requests if connector_param_max_requests else 0),
        connector_param_feedback_config
    )
except Exception as e:
    raise e

try:
    # This try block is for catching unexpected errors
    request_queue = queue.Queue(connector_config.max_requests)
    request_processor = SimpleRequestProcessor(
        request_queue=request_queue,
        model_input_uploader=model_input_uploader,
        model_prediction_publisher=model_prediction_publisher
    )

    # request_processor runs on a separate thread and listens for
    # events published to the request_queue.
    request_processor.start()
except Exception as e:
    raise e




def function_handler(event, context):
    # Validate input and return to client immediately if something is
    # wrong.
    try:
        request_id = context.aws_request_id
        if not request_id:
            raise ValueError("No aws_request_id was found in input context.")
    except Exception as e:
        raise e

    try:
        feedback_input = FeedbackInput(request_id, event, context.client_context.custom)
        if feedback_input.config_id not in connector_config.feedback_config_map:
            raise ValueError("Feedback configuration map does not contain config_id: {}".format(feedback_input.config_id))
        feedback_config = connector_config.feedback_config_map[feedback_input.config_id]
    except Exception as e:
        raise e

    try:
        logging.info("Enqueing request to be processed. Request Id: {}".format(request_id))
        request_queue.put_nowait((feedback_input, feedback_config))
    except queue.Full as e:
        raise e

    logging.info("Request has successfully be enqueued. Request Id: {}".format(request_id))
    return
