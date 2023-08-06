#!/usr/bin/env python
# -*- coding:utf-8 -*-
import functools
import json
import grpc

from .. import log
from ..error import Error, new_error, code_pb2

"""
python gRPC server example:
https://github.com/avinassh/grpc-errors/blob/HEAD/python
"""


class Status(grpc.Status):
    def __init__(self, code: grpc.StatusCode, details: str, trailing_metadata):
        self.code = code
        self.details = details
        self.trailing_metadata = trailing_metadata


def error_to_grpc_status(err: Error) -> grpc.Status:
    grpc_status_code = getattr(grpc.StatusCode, code_pb2.Code.Name(err.code))
    grpc_details = json.dumps({
        "message": err.message,
        "localized_message": err.localized_message
    })
    metadata = [(k, v) for k, v in err.metadata.items()]
    grpc_trailing_metadata = metadata + [("reason", str(err.reason))]
    return Status(grpc_status_code, grpc_details, tuple(grpc_trailing_metadata))


def grpc_exception_to_error(exception: grpc.RpcError) -> Error:
    """
    grpc.RpcError is grpc.Call, also Client-Side Context.
    https://grpc.github.io/grpc/python/grpc.html#client-side-context
    :param exception:
    :return:
    """
    error_code = exception.code().value[0]
    try:
        details = json.loads(exception.details())
    except json.decoder.JSONDecodeError:
        # in gRPC raw exception, details are utf-8 string.
        error_message = exception.details()
        error_localized_message = ""
    else:
        error_message = details.get("message", "")
        error_localized_message = details.get("localized_message", "")

    trailing_metadata = exception.trailing_metadata()
    error_metadata = {}
    error_reason = 0
    for i in trailing_metadata:
        if i.key == "reason":
            error_reason = int(i.value)
        else:
            error_metadata[i.key] = i.value

    if error_code in (code_pb2.INTERNAL, code_pb2.UNKNOWN):
        # get gRPC debug information
        error_metadata["debug_error_string"] = exception.debug_error_string()

    return new_error(
        error_code, error_reason, error_message,
        error_localized_message, error_metadata
    )


def grpc_execute(service_func):
    """
    接受grpc的请求，转换为Service的输入参数。调用Service的方法，捕获异常，处理Service错误
    转化为grpc的错误信息。返回grpc的response。
    """
    logger = log.get_root_logger()

    @functools.wraps(service_func)
    def wrapper_execute_service(self, request, context):
        try:
            # execute Service method
            response, err = service_func(self, request, context)
        except Exception as e:
            # generate error object
            class_name = self.__class__.__name__
            func_name = service_func.__name__
            func_doc = "%s.%s" % (class_name, func_name)
            exception_name = e.__class__.__name__
            err_msg = "Execute %s got %s: %s" % \
                      (func_doc, exception_name, e)
            logger.exception(err_msg)
            err = new_error(code_pb2.INTERNAL, 0, err_msg)
            context.abort_with_status(error_to_grpc_status(err))
        else:
            if err:
                # Service method return error
                context.abort_with_status(error_to_grpc_status(err))
            # check Service method return type
            if response is None:
                class_name = self.__class__.__name__
                func_name = service_func.__name__
                func_doc = "%s.%s" % (class_name, func_name)
                err_msg = "Execute %s should return Response, but got None." \
                          % func_doc
                logger.warning(err_msg)
                err = new_error(code_pb2.INTERNAL, 0, err_msg)
                context.abort_with_status(error_to_grpc_status(err))
            # return Service method response(grpc response)
            return response

    return wrapper_execute_service



