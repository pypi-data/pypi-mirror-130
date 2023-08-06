"""
Copyright 2021 Daniel Afriyie

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import pathlib
import os

from ru.utils import abstractmethod


class Logger:
    __loggers = {}

    def __init__(self, name: str = None, fmt: str = None, filename: str = None):
        self._name = name if name else __name__
        self._fmt = fmt if fmt else '%(asctime)s:%(levelname)s:%(message)s'
        self._filename = filename
        self._root_path = pathlib.Path('.').absolute()

    def _get_log_file(self):
        fn = self._filename if self._filename else 'log'
        log_path = os.path.join(self._root_path, 'logs')
        log_file = os.path.join(log_path, f'{fn}.log')
        if not os.path.exists(log_path):
            os.mkdir(os.path.join(log_path))
        return log_file

    def _create_logger(self):
        _logger = logging.getLogger(self._name)
        _logger.setLevel(level=logging.DEBUG)

        formatter = logging.Formatter(self._fmt)
        file_handler = logging.FileHandler(self._get_log_file())
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.INFO)

        _logger.addHandler(file_handler)
        _logger.addHandler(stream_handler)

        return _logger

    @abstractmethod
    def _log_file_manager(self):
        """
        check if the log file size is more than 10mb then deletes it
        """

    def __call__(self):
        if self._name in self.__loggers:
            return self.__loggers.get(self._name)
        else:
            _logger = self._create_logger()
            self.__loggers[self._name] = _logger
            return _logger


def logger(name: str = None, fmt: str = None, filename: str = None):
    lg = Logger(name, fmt, filename)
    return lg()
