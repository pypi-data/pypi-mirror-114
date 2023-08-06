# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import json
import logging
from datetime import datetime

from awsiot.greengrasscoreipc.model import (
    QOS,
    PublishToIoTCoreRequest
)

class ModelPredictionPublisher(object):
    def __init__(self, ipc_client):
        self._client = ipc_client

    def publish(self, config_id, model_prediction, model_input_location, metadata, timestamp=datetime.now()):
        topic = "feedback/message/prediction"
        request = PublishToIoTCoreRequest()
        TIMEOUT = 10
        qos = QOS.AT_LEAST_ONCE
        request.topic_name = topic
        request.qos = qos

        extra_metadata = {}

        if timestamp:
            extra_metadata["publish-ts"] = str(timestamp)

        metadata.update(extra_metadata)

        request.payload = bytes(json.dumps({
                "source-ref": model_input_location.uri,
                "model-prediction": model_prediction,
                "metadata": metadata,
                "config-id" : config_id
            }), "utf-8")

        operation = self._client.new_publish_to_iot_core()
        operation.activate(request)
        future = operation.get_response()
        future.result(TIMEOUT)

        logging.info("Published model prediction for S3 object: {}, to MQTT topic: {} for feedback config-id: {}".format(
            model_input_location.uri, topic, config_id
        ))
