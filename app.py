from flask import Flask, Response

from conf import s
from conntext import before_request, ServiceResponse, error_handler, after_request
from init_service import start_task
from log import logger
from route_list import ROUTE_LIST
import utils
import traceback


class WsgiApp(object):
    def __init__(self, app):
        self.app = app

    # 对header做特殊的处理
    def __call__(self, environ, start_response):
        try:
            # 对scheme的处理
            # script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
            # if script_name:
            #     environ["SCRIPT_NAME"] = script_name
            #     path_info = environ["PATH_INFO"]
            #     if path_info.startswith(script_name):
            #         environ["PATH_INFO"] = path_info[len(script_name) :]
            #
            # scheme = environ.get("HTTP_X_SCHEME", "")
            # if scheme:
            #     environ["wsgi.url_scheme"] = scheme
            return self.app(environ, start_response)
        except:
            logger.error("environ:{} ,err:{}".format(environ, traceback.format_exc()))
            return self.app(environ, start_response)

class ServiceCentre(Flask):
    def __init__(self):
        super().__init__(import_name=s.get_conf_str("SERVER_NAME", "v2ray_subscribe"))

        self._init_service()

    def make_response(self, rv):
        if isinstance(rv, ServiceResponse):
            return Response(rv.get_data(), mimetype="application/json", status=200)
        elif isinstance(rv, bytes):
            pass
        return super().make_response(rv)

    def _init_route_list(self):
        for ROUTE in ROUTE_LIST:
            logger.info("a new route will add {}".format(ROUTE.name))
            self.register_blueprint(ROUTE)

    def _init_service(self):
        self._init_route_list()
        self.logger = logger
        start_task()

        self.before_request_funcs.setdefault(None, []).append(before_request)
        self.after_request_funcs.setdefault(None, []).append(after_request)

        self._register_error_handler(None, Exception, error_handler)


app = ServiceCentre()
app.wsgi_app = WsgiApp(app.wsgi_app)
app.auto_find_instance_path()


@app.route("/favicon.ico")
def favicon():
    return ""


if __name__ == "__main__":
    app.run(
        s.get_conf_str("HOST", default="0.0.0.0"),
        port=s.get_conf_int("PORT", default=5000),
        threaded=True,
        debug=s.get_conf_bool("LOG_DEBUG", default=False),
    )

    # http_server = WSGIServer(
    #     (
    #         g.get_conf_str("HOST", default="0.0.0.0"),
    #         g.get_conf_int("PORT", default=5000),
    #     ),
    #     app,
    # )
    # http_server.serve_forever()
