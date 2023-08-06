# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import json
import logging
import numbers
import six

CLOUD_WATCH_NAME_SPACE = "GreengrassFeedbackConnector"
DIMENSION_FEEDBACK_CONFIG_ID = "FeedbackConfigId"
TOPIC_CLOUD_WATCH_CONNECTOR = "cloudwatch/metric/put"

class CWConnectorMetricsPublisher (object):

    def __init__(self, gg_client):
        self._iot_client = gg_client

    def _publish_message(self, payload):
        self._iot_client.publish(topic=TOPIC_CLOUD_WATCH_CONNECTOR, payload=json.dumps(payload))

    def _publish_value(self, metric_name, value, unit, config_id):
        logging.info("Publishing to Cloudwatch connector with metric_name: {}, value: {}, unit: {}, config_id: {}.".format(str(metric_name), str(value), str(unit), str(config_id)))

        dimensions = None
        if config_id:
            dimensions = []
            config_dimension = MetricDimension(DIMENSION_FEEDBACK_CONFIG_ID, config_id)
            dimensions.append(config_dimension)

        metric_data = MetricData(
            metric_name=metric_name, 
            value=value, 
            dimensions=dimensions, 
            unit=unit
        )

        request_message = CWConnectorMessage(
            namespace=CLOUD_WATCH_NAME_SPACE, 
            metric_data=metric_data
        )

        self._publish_message(request_message.json)

    def publish_counter(self, metric_name, value, config_id=None):
        self._publish_value(metric_name=metric_name, value=value, unit="Count", config_id=config_id)

    def publish_bytes(self, metric_name, value, config_id=None):
        self._publish_value(metric_name=metric_name, value=value, unit="Bytes", config_id=config_id)

class CWConnectorMessage (object):
    EXCEPTION_PREFIX = "Failed to construct CWConnectorMessage."

    def __init__(self, namespace, metric_data):
        if not isinstance(namespace, six.string_types):
            raise ValueError("{} Requires namespace to be of type string".format(
                self.EXCEPTION_PREFIX
            ))
        self._namespace = namespace

        if not isinstance(metric_data, MetricData):
            raise ValueError("{} Requires metric_data to be of type MetricData".format(
                self.EXCEPTION_PREFIX
            ))
        self._metric_data = metric_data

    @property
    def json(self):
        return {
            "request": {
                "namespace": self._namespace,
                "metricData": self._metric_data.json
            }
        }

class MetricData (object):
    EXCEPTION_PREFIX = "Failed to construct MetricData."

    def __init__(self, metric_name, value, dimensions=None, timestamp=None, unit=None):
        if not isinstance(metric_name, six.string_types):
            raise ValueError("{} Requires metric_name to be of type string".format(
                self.EXCEPTION_PREFIX
            ))
        self._metric_name = metric_name

        if not isinstance(value, numbers.Number):
            raise ValueError("{} Requires value to be of type number".format(
                self.EXCEPTION_PREFIX
            ))
        self._value = value

        if dimensions:
            if not isinstance(dimensions, list):
                raise ValueError("{} Requires dimensions to be a list".format(
                    self.EXCEPTION_PREFIX
                ))
            for dimension in dimensions:
                if not isinstance(dimension, MetricDimension):
                    raise ValueError("{} Requires dimension to be MetricDimension".format(
                        self.EXCEPTION_PREFIX
                    ))
        self._dimensions = dimensions

        if timestamp:
            if not isinstance(timestamp, float):
                raise ValueError("{} Requires timestamp to be of type float".format(
                    self.EXCEPTION_PREFIX
                ))
        self._timestamp = timestamp

        if unit:
            if not isinstance(unit, six.string_types):
                raise ValueError("{} Requires unit to be of type string".format(
                    self.EXCEPTION_PREFIX
                ))
        self._unit = unit

    @property
    def json(self):
        metric_data = {
            "metricName": self._metric_name,
            "value": self._value,
        }

        if self._dimensions:
            dimensions_to_add = []
            for dimension in self._dimensions:
                dimensions_to_add.append(dimension.json)
            metric_data["dimensions"] = dimensions_to_add

        if self._timestamp:
            metric_data["timestamp"] = self._timestamp

        if self._unit:
            metric_data["unit"] = self._unit

        return metric_data

class MetricDimension (object):
    def __init__(self, name, value):
        if not isinstance(name, six.string_types):
            raise ValueError("Found invalid metric dimension name. Name must be a string.")
        
        if not isinstance(value, six.string_types):
            raise ValueError("Found invalid metric dimension value. Value must be a string.")

        self._name = name
        self._value = value

    @property
    def json(self):
        return {
            "name": self._name,
            "value": self._value
        }
