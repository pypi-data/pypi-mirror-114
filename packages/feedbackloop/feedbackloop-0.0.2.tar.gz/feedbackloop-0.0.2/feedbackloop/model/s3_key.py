# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import os


class S3Key(object):
    def __init__(self, prefix, filename):
        self._key = os.path.join(prefix.strip('/'), filename.filename)

    @property
    def key(self):
        return self._key
