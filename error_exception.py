import utils


class InternalException(Exception):
    pass


_err_map = {
    -1: "system error",
}


def create_error(errcode: int != 0):
    errmsg = _err_map.get(errcode)
    create_error_with_msg(errcode, errmsg)


def create_error_with_msg(errcode: int != 0, errmsg: str != ""):
    raise InternalException(errcode, utils.encode_to_utf8(errmsg))
