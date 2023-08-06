# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Module represents the connectors configuration.
#

import re
import six
from DeepGreenFeedbackConnectorLambda.sampling.sampling_strategy import SamplingStrategyFactory

PARAM_S3_BUCKET = "s3-bucket-name"
PARAM_S3_PREFIX = "s3-prefix"
PARAM_FILE_EXTENSION = "file-ext"
PARAM_CONTENT_TYPE = "content-type"
PARAM_SAMPLING_STRATEGY = "sampling-strategy"
PARAM_SAMPLING_STRATEGY_NAME = "strategy-name"
PARAM_SAMPLING_RATE = "rate"
PARAM_SAMPLING_THRESHOLD = "threshold"

PATTERN_STRING_S3_BUCKET = "^[a-z0-9\.\-]{3,63}$"
PATTERN_S3_BUCKET = re.compile(PATTERN_STRING_S3_BUCKET)

COMMON_CONSTRUCTOR_ERR_MSG = "Failed to construct feedback configuration entry."


class FeedbackConfig (object):

    def __init__(self, feedback_config_entry_json):
        # Required parameters
        self._s3_bucket = feedback_config_entry_json[PARAM_S3_BUCKET]
        # Do basic regex checking for invalid characters and length
        if not PATTERN_S3_BUCKET.match(self._s3_bucket):
            raise ValueError("{} Found invalid S3 bucket name: {}".format(
                COMMON_CONSTRUCTOR_ERR_MSG, str(self._s3_bucket))
            )

        self._content_type = feedback_config_entry_json[PARAM_CONTENT_TYPE]
        if not isinstance(self._content_type, six.string_types):
            raise ValueError("{} Content type argument must be of type string.".format(COMMON_CONSTRUCTOR_ERR_MSG))

        # Optional parameters
        self._s3_prefix = feedback_config_entry_json.get(PARAM_S3_PREFIX)
        if self._s3_prefix:
            if not isinstance(self._s3_prefix, six.string_types):
                raise ValueError("{} S3 prefix argument must be of type string.".format(COMMON_CONSTRUCTOR_ERR_MSG))
        else:
            self._s3_prefix = ""

        self._file_ext = feedback_config_entry_json.get(PARAM_FILE_EXTENSION)
        if self._file_ext:
            if not isinstance(self._file_ext, six.string_types):
                raise ValueError("{} File extension argument must be of type string.".format(COMMON_CONSTRUCTOR_ERR_MSG))
        else:
            self._file_ext = ""

        sampling_strategy_config = feedback_config_entry_json.get(PARAM_SAMPLING_STRATEGY)
        if sampling_strategy_config:
            self._sampling_strategy = SamplingStrategyFactory.create_instance(
                strategy_name=sampling_strategy_config[PARAM_SAMPLING_STRATEGY_NAME],
                rate=sampling_strategy_config.get(PARAM_SAMPLING_RATE),
                threshold=sampling_strategy_config.get(PARAM_SAMPLING_THRESHOLD)
            )
        else:
            self._sampling_strategy = None

    @property
    def s3_bucket(self):
        return self._s3_bucket

    @property
    def s3_prefix(self):
        return self._s3_prefix

    @property
    def file_ext(self):
        return self._file_ext

    @property
    def content_type(self):
        return self._content_type

    @property
    def sampling_strategy(self):
        return self._sampling_strategy
