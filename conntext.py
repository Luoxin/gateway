import json

from flask import request, jsonify, ctx, g

import utils
from error_exception import InternalException
from log import logger


class ServiceResponse(object):
    def __init__(self, response=None):
        if response is None or isinstance(response, dict):
            self.response = json.dumps({"data": response, "errcode": 0, "errmsg": ""})
        else:
            self.response = response

    def get_data(self):
        return self.response


def after_request(response):
    if request.path == "/favicon.ico":
        return

    method = request.method

    # 获取请求参数
    request_message = ""
    if method == "GET":
        request_message = request.args.to_dict()
    elif method == "POST":
        if request.json is not None:
            request_message = request.json
        elif request.form is not None:
            request_message = request.form

    # 获取请求用户的真实ip地址
    real_ip = request.remote_addr
    if request.headers.get("X-Forwarded-For") is not None:
        real_ip = request.headers.get("X-Forwarded-For")

    rsp_msg = response.response
    if isinstance(rsp_msg, (list, set, tuple)):
        rsp_msg = " ".join([item.decode("utf-8") for item in rsp_msg])
    else:
        logger.warning("response type {} not ")

    logger.info(
        "{}  Path: {}  Method: {} RemoteAddr: {} Headers: {} RequestSize: {} RequestMsg: {} ResponseMsg {}".format(
            g.get("id"),
            request.path,
            request.method,
            real_ip,
            request.headers.to_wsgi_list(),
            request.content_length,
            request_message,
            rsp_msg
            # , request.__dict__
        )
    )

    return response


def before_request():
    if request.path == "/favicon.ico":
        return

    req_id = request.headers.get("X-Req-Id", "", str)
    if req_id is None or req_id == "":
        req_id = utils.gen_uuid()

    g.setdefault("id", req_id)

    method = request.method

    # 获取请求参数
    request_message = ""
    if method == "GET":
        request_message = request.args.to_dict()
    elif method == "POST":
        if request.json is not None:
            request_message = request.json
        elif request.form is not None:
            request_message = request.form

    if isinstance(request_message, (list, tuple, set)):
        request_message = " ".join(request_message)
    elif isinstance(request_message, dict):
        request_message = json.dumps(request_message)

    # 获取请求用户的真实ip地址
    real_ip = request.remote_addr
    if request.headers.get("X-Forwarded-For") is not None:
        real_ip = request.headers.get("X-Forwarded-For")

    logger.info(
        "{} Path: {}  Method: {} RemoteAddr: {} Headers: {} RequestSize: {} RequestMessage: {}  ".format(
            req_id,
            request.path,
            request.method,
            real_ip,
            request.headers.to_wsgi_list(),
            request.content_length,
            request_message
            # , request.__dict__
        )
    )


def error_handler(e):
    logger.error("err:{}".format(e))

    response_data = {"data": {}, "errcode": 0, "errmsg": ""}
    if isinstance(e, InternalException):
        response_data["errcode"] = e.args[0]
        response_data["errmsg"] = e.args[1]
    elif isinstance(e, ctx.HTTPException):
        response_data["errcode"] = e.code
        response_data["errmsg"] = e.description
    else:
        response_data["errcode"] = -1
        response_data["errmsg"] = "system error:{}".format(e)

    logger.error("err:{}".format(response_data))
    return jsonify(response_data)
