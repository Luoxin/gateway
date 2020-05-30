from flask import Blueprint, request
from utils import logger  # 日志
from error_exception import create_error_with_msg

gateway_api = Blueprint("gateway", __name__)


@gateway_api.route(
    "/gateway/",
    defaults={"path": ""},
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "COPY"],
)
@gateway_api.route(
    "/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "COPY"]
)
def gateway(path):
    print(path)
    scheme = request.scheme
    if scheme == "http":
        pass
    else:
        return ""

    return ""
