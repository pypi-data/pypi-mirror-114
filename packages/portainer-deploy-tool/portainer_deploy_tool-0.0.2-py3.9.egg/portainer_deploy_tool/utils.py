import requests
from pyloggerhelper import log

base_schema_properties = {
    "log_level": {
        "type": "string",
        "title": "l",
        "description": "log等级",
        "enum": ["DEBUG", "INFO", "WARN", "ERROR"],
        "default": "DEBUG"
    },
    "base_url": {
        "type": "string",
        "title": "b",
        "description": "portainer的根url"
    },
    "retry_max_times": {
        "type": "integer",
        "description": "重试次数",
    },
    "retry_interval_backoff_factor": {
        "type": "number",
        "description": "重试间隔时间,的参数,间隔时间位`{backoff factor} * (2 ** ({number of total retries} - 1))`",
        "default": 0.1
    }
}


class HttpCodeError(Exception):
    """http请求返回错误"""
    pass


def get_jwt(rq: requests.Session, base_url: str, username: str, password: str) -> str:
    """获取jwt.

    Args:
        rq (requests.Session): 请求会话
        base_url (str): portainer的根地址
        username (str): portainer用户名
        password (str): 用户的密码

    Returns:
        str: jwt的值
    """
    res = rq.post(
        base_url + "/api/auth",
        json={
            "Username": username,
            "Password": password
        }
    )
    if res.status_code != 200:
        log.error("get jwt query get error",
                  base_url=base_url,
                  username=username,
                  status_code=res.status_code)
        raise HttpCodeError("get jwt query get error")
    try:
        res_json = res.json()
    except Exception as e:
        log.error("get jwt query get json result error",
                  base_url=base_url,
                  username=username,
                  err=type(e),
                  err_msg=str(e),
                  exc_info=True,
                  stack_info=True)
        raise e
    else:
        jwt = res_json.get("jwt")
        if jwt:
            return jwt
        else:
            log.error("get jwt query has no field jwt",
                      base_url=base_url,
                      username=username,
                      res_json=res_json)
            raise AttributeError("get jwt query has no field jwt")
