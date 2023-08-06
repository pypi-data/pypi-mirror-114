# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import json
import logging
import connector_lambda_python_commons.response as StatusResponse
from abc import ABCMeta, abstractmethod

STATUS_TOPIC = "feedback/message/status"

FIELD_S3_RESPONSE = "s3_response"
VALUE_SAMPLE_DROPPED = "sample_dropped_by_strategy"

class StatusMessage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def payload(self):
        pass

class StatusMessageSuccess(StatusMessage):
    def __init__(self, request_id, s3_response_json):
        response_fields = {
            FIELD_S3_RESPONSE : s3_response_json
        }
        self._response = StatusResponse.generate_success_response(request_id, **response_fields)

    @property
    def payload(self):
        return json.dumps(self._response)


class StatusMessageSampleDropped(StatusMessage):
    def __init__(self, request_id):
        success_message = StatusResponse.generate_success_response(request_id)
        success_message[StatusResponse.RESPONSE_FIELD_STATUS] = VALUE_SAMPLE_DROPPED
        self._response = success_message

    @property
    def payload(self):
        return json.dumps(self._response)

class StatusMessageError(StatusMessage):
    def __init__(self, request_id, exception, message):
        if not isinstance(exception, Exception):
            raise ValueError("StatusMessageError requires exception to be of type Exception.")
        self._response = StatusResponse.generate_error_response(request_id, type(exception).__name__, message)

    @property
    def payload(self):
        return json.dumps(self._response)

class StatusPublisher(object):
    def __init__(self, iot_client):
        self._client = iot_client

    def publish(self, status_message):
        if not isinstance(status_message, StatusMessage):
            raise ValueError("status_message must be of type StatusMessage.")

        logging.info("Publishing status message to topic: {}, with message payload: {}".format(
            STATUS_TOPIC, str(status_message.payload)
        ))
        self._client.publish(topic=STATUS_TOPIC, payload=status_message.payload)