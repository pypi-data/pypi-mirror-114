# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import logging
import sys

COUNTER_UPLOAD_OBJECT_SUCCESS = "SampleUploadSuccess"
COUNTER_UPLOAD_OBJECT_FAILURE = "SampleUploadFailure"
BYTES_SAMPLE_SIZE = "SampleSize"

RESPONSE_KEY_S3_BUCKET = "bucket"
RESPONSE_KEY_S3_KEY = "key"

class ModelInputUploader(object):
    '''
        Responsible for uploading the input of ML models
        to S3. Ex. image, sound clip, etc
    '''
    def __init__(self, s3_client, cw_metrics_publisher):
        self._client = s3_client
        self._metrics_publisher = cw_metrics_publisher

    def upload(self, s3_location, payload, content_type, metadata):
        # Publish size of payload on every request. This may provide
        # a useful hint in case of upload failures.
        self._metrics_publisher.publish_bytes(BYTES_SAMPLE_SIZE, sys.getsizeof(payload))
        try:
            response = self._client.put_object(
                Body=payload,
                Bucket=s3_location.bucket,
                ContentType=content_type,
                Key=s3_location.key.key,
                Metadata=metadata if metadata else {}
            )

            # Add extra fields to the response
            response[RESPONSE_KEY_S3_BUCKET] = s3_location.bucket
            response[RESPONSE_KEY_S3_KEY] = s3_location.key.key

            logging.info("Successfully uploaded model input to S3 location: {}, with response: {}".format(str(s3_location.uri), str(response)))
            self._metrics_publisher.publish_counter(COUNTER_UPLOAD_OBJECT_SUCCESS, 1)
            return response
        except Exception as e:
            logging.warn("Failed to upload object to S3 location: {}, with exception type: {}, error: {}.".format(str(s3_location.uri), type(e).__name__, e))
            self._metrics_publisher.publish_counter(COUNTER_UPLOAD_OBJECT_FAILURE, 1)
            raise e