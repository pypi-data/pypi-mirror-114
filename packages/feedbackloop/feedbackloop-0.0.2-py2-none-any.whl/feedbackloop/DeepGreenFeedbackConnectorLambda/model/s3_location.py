# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import six
from DeepGreenFeedbackConnectorLambda.model.s3_key import S3Key

class S3Location(object):
    def __init__(self, bucket, key):
        if not isinstance(bucket, six.string_types):
            raise ValueError("Failed to create S3Location. Parameter 'bucket' must be of type string.")

        if not isinstance(key, S3Key):
            raise ValueError("Failed to create S3Location. Parameter 'key' must be of type S3Key.")

        self._bucket = bucket
        self._key = key

    @property
    def bucket(self):
        return self._bucket
    
    @property
    def key(self):
        return self._key
    
    @property
    def uri(self):
        return "s3://{}/{}".format(self._bucket, self._key.key)