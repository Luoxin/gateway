import traceback

import requests
import werkzeug
from flask import request, abort, Blueprint, make_response, ctx
from werkzeug.exceptions import NotFound as HttpNotFound

from conf import g
from error_exception import create_error, InternalException
from utils import logger

gateway_api = Blueprint("gateway", __name__)

dns_map = {"api.devluoxin.cn": "203.195.187.254:3000"}

route_map = {}


@gateway_api.route(
    "/gateway/",
    defaults={"path": ""},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "COPY"],
)
@gateway_api.route(
    "/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "COPY"]
)
def gateway(path):
    rsp = ""

    scheme = request.scheme
    if scheme == "http":
        host = request.host
        path = request.full_path
        method = request.method
        req_headers = {h[0]: h[1] for h in request.headers}
        data = request.data or request.form or None

        # 自定义dns
        # host = g.dns_cache.get(host, host)
        host = "203.195.187.254:3000"

        # 去掉gateway
        path = path.replace("/gateway/", "/", 1)

        # TODO 对header做一些特殊操作

        try:
            with requests.request(
                method,
                "{}://{}{}".format(scheme, host, path),
                headers=req_headers,
                data=data,
                stream=True,
                timeout=5,
            ) as r:
                if r.status_code != 200:
                    create_error(-1)

                rsp_headers = {h[0]: h[1] for h in r.headers}

                rsp = make_response(r.content)
                # TODO 对返回的header做特殊的操作
                # rsp.headers["X-Req-Id"] = utils.gen_uuid()

                rsp.headers = werkzeug.datastructures.Headers(rsp_headers)
        except:
            logger.error("err:{}".format(traceback.format_exc()))
            create_error(-1)

    return rsp
