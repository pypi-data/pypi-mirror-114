import logging
import uuid
from threading import Thread
from DeepGreenFeedbackConnectorLambda.model.feedback_input import FeedbackInput
from DeepGreenFeedbackConnectorLambda.model.feedback_input import PARAM_REQUEST_ID
from DeepGreenFeedbackConnectorLambda.model.filename import Filename
from DeepGreenFeedbackConnectorLambda.model.s3_key import S3Key
from DeepGreenFeedbackConnectorLambda.model.s3_location import S3Location
from DeepGreenFeedbackConnectorLambda.service.model_input_uploader import ModelInputUploader

COUNTER_SAMPLE_NOT_USED = "SampleNotUsed"
COUNTER_PUBLISHED_SAMPLE_AND_PREDICTION = "SampleAndPredictionPublished"


class SimpleRequestProcessor(Thread):
    '''
        Responsible for handling the resource intensive aspects of feedback upload
        requests (S3 upload and model prediction publishing)
    '''
    def __init__(
            self,
            request_queue,
            model_input_uploader,
            model_prediction_publisher
    ):
        Thread.__init__(self)
        self._request_queue = request_queue
        self._model_input_uploader = model_input_uploader
        self._model_prediction_publisher = model_prediction_publisher

    def _handle(self, feedback_input, feedback_config):
        request_id = feedback_input.request_id
        sampling_strategy = feedback_config.sampling_strategy

        # If no filename argument is given to S3Key, a UUID will be used
        filename = Filename(str(uuid.uuid4()), feedback_config.file_ext)
        s3_key = S3Key(prefix=feedback_config.s3_prefix, filename=filename)
        model_input_upload_location = S3Location(feedback_config.s3_bucket, s3_key)
        if not sampling_strategy or sampling_strategy.should_use_sample(feedback_input.model_prediction):
            try:
                upload_result = self._model_input_uploader.upload(
                    s3_location=model_input_upload_location,
                    payload=feedback_input.model_input,
                    content_type=feedback_config.content_type,
                    metadata=feedback_input.metadata
                )
            except Exception as e:
                error_str = "[RequestId: {}] Failed to upload model input data due to exception. Model prediction will not be published. Exception type: {}, error: {}".format(
                    request_id, type(e).__name__, e
                )
                logging.warn(error_str)

            else:
                try:
                    self._model_prediction_publisher.publish(
                        config_id=feedback_input.config_id,
                        model_prediction=feedback_input.model_prediction,
                        model_input_location=model_input_upload_location,
                        metadata=feedback_input.metadata
                    )
                except Exception as e:
                    logging.warn(
                        "[RequestId: {}] Unexpected exception raised while publishing Predictions. Exception type: {}, error: {}".format(
                            request_id, type(e).__name__, e
                        ))
                success_str = "[RequestId: {}] Successfully uploaded model input and published model prediction.".format(request_id)
                logging.info(success_str)

        else:
            logging.info(
                "[RequestId: {}] Model input and model prediction were dropped by the configured sampling strategy for feedback configuration with id: {}".format(
                    request_id, feedback_input.config_id))

    def _process_input(self):
        # Queue::get will default to blocking if the queue is empty
        feedback_input, feedback_config = self._request_queue.get()
        request_id = feedback_input.request_id
        try:
            logging.info("[RequestId: {}] Processing request.".format(request_id))
            self._handle(feedback_input, feedback_config)
        except Exception as e:
            logging.warn(
                "[RequestId: {}] Unexpected exception raised while processing request. Exception type: {}, error: {}".format(
                    request_id, type(e).__name__, e
                ))
        finally:
            # call task done to indicate to queue that request
            # has been processed.
            logging.info("[RequestId: {}] Finished processing request.".format(request_id))
            self._request_queue.task_done()

    def run(self):
        while True:
            self._process_input()



