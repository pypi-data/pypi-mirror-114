# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import re
import six

PATTERN_STRING_CONFIG_ID = "^[a-zA-Z0-9][a-zA-Z0-9-]{1,62}$"
PATTERN_CONFIG_ID = re.compile(PATTERN_STRING_CONFIG_ID)


class ConfigId(object):
    '''
        Responsible for validating and storing a feedback
        configuration id. Valid ids must be:
        1. At least 2 characters
        2. Less than or equal to 63 characters
        3. Lead with a lower/upper case letter or number
        4. Contain lower/upper case letters, numbers, or hyphens
        Examples:
          config-a
          Config-1
          id0
    '''
    def __init__(self, config_id_str):
        if not isinstance(config_id_str, six.string_types) or not PATTERN_CONFIG_ID.match(config_id_str):
            raise ValueError(
                "Failed to create config id. Config id is invalid: {}. Config id must match: {}".format(
                    str(config_id_str), PATTERN_STRING_CONFIG_ID
                )
            )
        self._id = config_id_str

    @property
    def id(self):
        return self._id
