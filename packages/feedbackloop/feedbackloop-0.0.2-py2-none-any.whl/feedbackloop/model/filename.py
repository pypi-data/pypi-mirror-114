# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.


class Filename(object):
    def __init__(self, filename, file_extension):
        if file_extension:
            stripped_file_extension = file_extension.strip('.')
            self._filename = "{}.{}".format(filename, stripped_file_extension)
        else:
            self._filename = filename

    @property
    def filename(self):
        return self._filename
