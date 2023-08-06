#!/usr/bin/env python
# -*- coding:utf-8 -*-

# for other package import
from . import error_pb2
from .error_pb2 import Error
from . import error_reason_pb2
from .error_reason_pb2 import ERROR_REASON_UNSPECIFIED


def new_error(code: int, reason: int,
              message="", localized_message="",
              metadata: dict = None) -> error_pb2.Error:
    """

    :param code:
    :param message:
    :param reason:
    :param localized_message:
    :param metadata: data format {"key": "value"}
    :return:
    """
    if metadata is None:
        metadata = {}
    else:
        # check metadata data type
        for k, v in metadata.items():
            if not isinstance(k, str) and not isinstance(k, bytes):
                raise TypeError("metadata key must be bytes or unicode")
            if not isinstance(v, str) and not isinstance(v, bytes):
                raise TypeError("metadata value must be bytes or unicode")

    return error_pb2.Error(
        code=code,
        message=message,
        reason=reason,
        localized_message=localized_message,
        metadata=metadata
    )
