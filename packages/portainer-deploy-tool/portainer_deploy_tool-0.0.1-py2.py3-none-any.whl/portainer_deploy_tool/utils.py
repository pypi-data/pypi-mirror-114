import time
from dataclasses import dataclass
import requests as rq
from pyloggerhelper import log
from typing import Dict, Any, List, Union, Optional

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
    }
}


class HttpCodeError(Exception):
    """http请求返回错误"""
    pass


class NotSwarmEndpointError(Exception):
    """节点不是swarm节点"""
    pass


@dataclass
class GitStackInfo:
    endpoint_id: int
    stack_name: str
    stack_id: Optional[int] = None
    swarm_id: Optional[str] = None
    composeFilePathInRepository: Optional[str] = None
    repositoryReferenceName: Optional[str] = None
    repositoryURL: Optional[str] = None
    env: Optional[List[Dict[str, str]]] = None

    def check_git_repository(self) -> None:
        if not (self.composeFilePathInRepository and self.repositoryReferenceName and self.repositoryURL):
            raise AttributeError("need git repository info")

    def update_to_portainer(self, base_url: str, jwt: str, prune: bool = False,
                            repositoryUsername: Optional[str] = None, repositoryPassword: Optional[str] = None) -> None:
        """更新portainer中的stack

        Args:
            base_url (str): portainer的根地址
            jwt (str): 访问jwt
            prune (bool, optional): 更新是否删除不再使用的资源. Defaults to False.
            repositoryUsername (Optional[str], optional): git仓库账户. Defaults to None.
            repositoryPassword (Optional[str], optional): git仓库密码. Defaults to None.

        Raises:
            HttpCodeError: update stack query get error
            e: update stack query get json result error
        """
        body: Dict[str, Any] = {
            "env": self.env,
            "prune": prune,
            "repositoryReferenceName": self.repositoryReferenceName,
        }
        if repositoryUsername and repositoryPassword:
            repositoryAuthentication = True
            body.update({
                "repositoryAuthentication": repositoryAuthentication,
                "repositoryPassword": repositoryPassword,
                "repositoryUsername": repositoryUsername
            })
        else:
            repositoryAuthentication = False
            body.update({
                "repositoryAuthentication": repositoryAuthentication
            })
        res = rq.put(
            f"{base_url}/api/stacks/{self.stack_id}/git",
            headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
            params={
                "endpointId": self.endpoint_id
            },
            json=body)
        if res.status_code != 200:
            log.error("update stack query get error",
                      base_url=base_url,
                      status_code=res.status_code,
                      stack=self)
            raise HttpCodeError("update stack query get error")
        try:
            res_json = res.json()
        except Exception as e:
            log.error("update stack query get json result error", stack=self, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
            raise e
        else:
            log.info("update stack ok", stack=self, result=res_json)

    def create_to_portainer(self, base_url: str, jwt: str,
                            repositoryUsername: Optional[str] = None, repositoryPassword: Optional[str] = None) -> None:
        """使用对象的信息创建stack.

        Args:
            base_url (str):  portainer的根地址
            jwt (str): 访问jwt
            repositoryUsername (Optional[str], optional): git仓库账户. Defaults to None.
            repositoryPassword (Optional[str], optional): git仓库密码. Defaults to None.

        Raises:
            AttributeError: only create git repository method
            HttpCodeError: create stack query get error
            e: create stack query get json result error
        """
        body: Dict[str, Any] = {
            "env": self.env,
            "composeFilePathInRepository": self.composeFilePathInRepository,
            "name": self.stack_name,
            "repositoryReferenceName": self.repositoryReferenceName,
            "repositoryURL": self.repositoryURL,
        }
        if repositoryUsername and repositoryPassword:
            repositoryAuthentication = True
            body.update({
                "repositoryAuthentication": repositoryAuthentication,
                "repositoryPassword": repositoryPassword,
                "repositoryUsername": repositoryUsername
            })
        else:
            repositoryAuthentication = False
            body.update({
                "repositoryAuthentication": repositoryAuthentication
            })
        if self.swarm_id:
            stack_type = 1
            body.update({"swarmID": self.swarm_id})
        else:
            stack_type = 2
        params = (("method", "repository"), ("type", stack_type), ("endpointId", self.endpoint_id))
        res = rq.post(
            f"{base_url}/api/stacks",
            headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
            params=params,
            json=body)
        if res.status_code != 200:
            log.error("create stack query get error",
                      base_url=base_url,
                      status_code=res.status_code,
                      stack=self)
            raise HttpCodeError("create stack query get error")
        try:
            res_json = res.json()
        except Exception as e:
            log.error("create stack query get json result error", stack=self, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
            raise e
        else:
            log.info("create stack ok", stack=self, result=res_json)

    def update_or_create(self, base_url: str, jwt: str, prune: bool = False,
                         repositoryUsername: Optional[str] = None, repositoryPassword: Optional[str] = None,
                         retry_max_times: Optional[int] = None, retry_interval: Union[int, float] = 3) -> None:
        self.check_git_repository()
        if retry_max_times and int(retry_max_times) > 0:
            for rt in range(int(retry_max_times)):
                try:
                    if self.stack_id:
                        self.update_to_portainer(base_url=base_url, jwt=jwt, prune=prune, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
                    else:
                        self.create_to_portainer(base_url=base_url, jwt=jwt, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
                except HttpCodeError as he:
                    raise he
                except Exception as e:
                    log.warn("update_or_create query get error, retry", retry_times=rt + 1, retry_max_times=int(retry_max_times),
                             err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
                    time.sleep(retry_interval)
                    continue
                else:
                    break
            log.info("update_or_create query ok")

        else:
            if self.stack_id:
                self.update_to_portainer(base_url=base_url, jwt=jwt, prune=prune, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
            else:
                self.create_to_portainer(base_url=base_url, jwt=jwt, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
            log.info("update_or_create query ok")


def get_jwt(base_url: str, username: str, password: str) -> str:
    """获取jwt.

    Args:
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


def get_swarm_id(base_url: str, jwt: str, endpoint: int) -> str:
    """获取端点的SwarmID.

    Args:
        base_url (str): portainer的根地址
        jwt (str): 访问jwt
        endpoint (int): 端点ID

    Raises:
        HttpCodeError: get swarm id query get error
        e: get swarm id query get json result error
        AssertionError: endpint not swarm

    Returns:
        str: Swarm ID
    """
    res = rq.get(f"{base_url}/api/endpoints/{endpoint}/docker/swarm",
                 headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}))
    if res.status_code != 200:
        log.error("get swarm id query get error",
                  base_url=base_url,
                  endpoint=endpoint,
                  status_code=res.status_code)
        raise HttpCodeError("get swarm id query get error")
    try:
        res_json = res.json()
    except Exception as e:
        log.error("get swarm id query get json result error", endpoint=endpoint, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
        raise e
    else:
        swarm_id = res_json.get("ID")
        if swarm_id:
            return swarm_id
        else:
            raise NotSwarmEndpointError(f"endpint {endpoint} not swarm")


def get_all_stacks_from_portainer(base_url: str, jwt: str) -> Dict[int, Dict[str, GitStackInfo]]:
    """

    Args:
        base_url (str): portainer的根地址
        jwt (str): 访问jwt

    Raises:
        HttpCodeError: get stack query get error
        e: get stack query get json result error

    Returns:
        Dict[int, Dict[str, GitStackInfo]]: dict[endpointid,dict[stack_name,stackinfo]]
    """
    res = rq.get(f"{base_url}/api/stacks",
                 headers=rq.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}))
    if res.status_code != 200:
        log.error("get swarm id query get error",
                  base_url=base_url,
                  status_code=res.status_code)
        raise HttpCodeError("get stack query get error")
    try:
        res_jsons = res.json()
    except Exception as e:
        log.error("get stack query get json result error", err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
        raise e
    else:
        result: Dict[int, Dict[str, GitStackInfo]] = {}
        for res_json in res_jsons:
            gcf = res_json.get('GitConfig')
            endpoint_id = res_json['EndpointId']
            stack_id = res_json['Id']
            stack_name = res_json["Name"]
            if gcf:
                gsi = GitStackInfo(
                    endpoint_id=endpoint_id,
                    env=res_json["Env"],
                    stack_id=stack_id,
                    stack_name=stack_name,
                    swarm_id=res_json.get('SwarmId'),
                    composeFilePathInRepository=gcf["ConfigFilePath"],
                    repositoryReferenceName=gcf["ReferenceName"],
                    repositoryURL=gcf["URL"]
                )
            else:
                gsi = GitStackInfo(
                    endpoint_id=endpoint_id,
                    env=res_json["Env"],
                    stack_id=stack_id,
                    stack_name=res_json["Name"],
                    swarm_id=res_json.get('SwarmId'),
                    composeFilePathInRepository=None,
                    repositoryReferenceName=None,
                    repositoryURL=None
                )
            if not result.get(endpoint_id):
                result[endpoint_id] = {stack_name: gsi}
            else:
                result[endpoint_id][stack_name] = gsi

        return result
