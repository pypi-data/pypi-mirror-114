# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Module represents the feedback connector's configuration.
#

import json

from feedbackloop.model.feedback_config import FeedbackConfig
from feedbackloop.model.config_id import ConfigId

PARAM_FEEDBACK_CONFIG_MAP = "FEEDBACK_CONFIGURATION_MAP"
PARAM_MAX_REQUESTS = "REQUEST_LIMIT"

ERROR_PREFIX_CONSTRUCT_MAP = "Failed to build feedback configuration map."


class ConnectorConfig (object):
    def __init__(self, max_requests, feedback_config_json_str):
        if not isinstance(max_requests, int):
            raise ValueError("Failed to parse connector configuration. Max requests must be of type 'int'.")
        self._max_requests = max_requests
        # load json with custom hook to raise on
        # duplicate config ids.

        feedback_config_map_json = json.loads(
            feedback_config_json_str,
            object_pairs_hook=ConnectorConfig._load_json_raise_on_duplicate_keys
        )
        if not isinstance(feedback_config_map_json, dict):
            raise ValueError("Failed to parse connector configuration. Feedback configuration JSON must be a valid dict.")

        self._feedback_config_map = self._build_feedback_config_map(feedback_config_map_json)

    @staticmethod
    def _load_json_raise_on_duplicate_keys(key_values):
        json_map = {}
        for key, value in key_values:
            if key in json_map:
                raise ValueError("{} Found duplicate keys: {}. Keys must be unique.".format(
                    ERROR_PREFIX_CONSTRUCT_MAP, str(key))
                )
            else:
                json_map[key] = value
        return json_map

    @staticmethod
    def _build_feedback_config_map(feedback_config_map_json):
        '''
            Marshals raw json map into Map<config-id, FeedbackConfig>
        '''
        feedback_config_map = {}
        for config_id_str, config_entry_json in feedback_config_map_json.items():
            config_id = ConfigId(config_id_str)
            feedback_config = FeedbackConfig(config_entry_json)
            feedback_config_map[config_id.id] = feedback_config
        if not feedback_config_map:
            raise ValueError("{} Failed to build feedback configuration list. No configurations specified.".format(
                ERROR_PREFIX_CONSTRUCT_MAP
            ))

        return feedback_config_map

    @property
    def max_requests(self):
        return self._max_requests

    @property
    def feedback_config_map(self):
        '''
            Returns Map<Feedback_Config_Id, FeedbackConfig>
        '''
        return self._feedback_config_map
