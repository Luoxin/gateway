import traceback

import requests
from flask import request, abort, Blueprint, make_response

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
    scheme = request.scheme
    if scheme == "http":
        host = request.host
        path = request.full_path
        method = request.method
        headers = request.headers
        data = request.data or request.form or None

        # 自定义dns
        host = dns_map.get(host) if dns_map.get(host) is not None else host

        # 去掉gateway
        path = path.replace("/gateway/", "/", 1)

        # TODO 对header做一些特殊操作

        try:
            r = requests.request(
                method,
                "{}://{}{}".format(scheme, host, path),
                headers=headers,
                data=data,
                stream=True,
                timeout=5,
            )

            rsp = make_response(r.content)
            rsp.status_code = r.status_code

            # TODO 对返回的header做特殊的操作
            # rsp.headers["X-Req-Id"] = utils.gen_uuid()

            return rsp
        except:
            logger.error("err:{}".format(traceback.format_stack()))

    else:
        pass

    abort(404)
