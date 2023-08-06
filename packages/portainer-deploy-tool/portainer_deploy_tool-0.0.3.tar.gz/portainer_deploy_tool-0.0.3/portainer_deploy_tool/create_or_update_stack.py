from pathlib import Path
from dataclasses import dataclass
from copy import deepcopy
from collections import defaultdict
from typing import Dict, Any, List, NamedTuple, DefaultDict, Optional
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from schema_entry import EntryPoint
from pyloggerhelper import log
from .utils import (
    HttpCodeError,
    base_schema_properties,
    get_jwt
)


schema_properties: Dict[str, Any] = {
    "username": {
        "type": "string",
        "title": "u",
        "description": "portainer的登录用户名"
    },
    "password": {
        "type": "string",
        "title": "p",
        "description": "portainer的登录用户名对应的密码",
    },
    "endpoints": {
        "type": "array",
        "title": "d",
        "description": "指定要部署的节点",
        "items": {
            "type": "integer"
        }
    },
    "excepts": {
        "type": "array",
        "title": "e",
        "description": "指定部署节点上排除哪些stack不要进行操作,格式为`endpoint::stackname`.",
        "items": {
            "type": "string"
        }
    },
    "suffix": {
        "type": "string",
        "title": "s",
        "description": "用于匹配的文件文件名后缀,注意除去后缀外的部分会作为stack名,而stack名中不能有`.`",
        "default": ".docker-compose.yaml"
    },
    "prune": {
        "type": "boolean",
        "description": "更新时是否清除不用的资源",
        "default": False

    },
    "repository_reference_name": {
        "type": "string",
        "description": "分支信息",
        "default": "refs/heads/master"
    },
    "repository_url": {
        "type": "string",
        "description": "git仓库根路径"
    },
    "repository_username": {
        "type": "string",
        "description": "git仓库用户名",
    },
    "repository_password": {
        "type": "string",
        "description": "git仓库用户名对应的密码",
    },
    "cwd": {
        "type": "string",
        "description": "执行位置",
        "default": "."
    }
}

schema_properties.update(**base_schema_properties)


class NotSwarmEndpointError(Exception):
    """节点不是swarm节点"""
    pass


class ComposeInfo(NamedTuple):
    stack_name: str
    path: str


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

    def update_to_portainer(self, rq: requests.Session, base_url: str, jwt: str, prune: bool = False,
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
            headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
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

    def create_to_portainer(self, rq: requests.Session, base_url: str, jwt: str,
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
            headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
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

    def update_or_create(self, rq: requests.Session, base_url: str, jwt: str, prune: bool = False,
                         repositoryUsername: Optional[str] = None, repositoryPassword: Optional[str] = None) -> None:
        self.check_git_repository()
        if self.stack_id:
            self.update_to_portainer(rq=rq, base_url=base_url, jwt=jwt, prune=prune, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
        else:
            self.create_to_portainer(rq=rq, base_url=base_url, jwt=jwt, repositoryUsername=repositoryUsername, repositoryPassword=repositoryPassword)
        log.info("update_or_create query ok")


class CreateOrUpdateStack(EntryPoint):
    """扫描指定目录下的compose文件,在指定的端点中如果已经部署则更新stack,否则创建stack."""
    default_config_file_paths = [
        "./create_or_update_stack_config.json"
    ]
    argparse_noflag = "endpoints"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["base_url", "username", "password", "endpoints", "suffix", "cwd", "repository_reference_name", "repository_url"],
        "properties": schema_properties
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.compose_infos: List[ComposeInfo] = []

    def find_compose(self, cwd: Path, suffix: str, root: Path) -> None:
        for p in cwd.iterdir():
            if p.is_file:
                if p.name.endswith(suffix):
                    rp = p.relative_to(root)
                    stack_name = p.name.replace(suffix, "")
                    if stack_name in [i.stack_name for i in self.compose_infos]:
                        log.error("stack name repetition", stack_name=stack_name)
                        raise AttributeError("stack name repetition")
                    ci = ComposeInfo(stack_name=stack_name, path=str(rp))
                    self.compose_infos.append(ci)
            elif p.is_dir():
                self._find_compose(cwd=p, suffix=suffix, root=root)

    def handdler_excepts(self, excepts: Optional[List[str]] = None) -> DefaultDict[int, List[ComposeInfo]]:
        result: DefaultDict[int, List[ComposeInfo]] = defaultdict(lambda: deepcopy(self.compose_infos))
        if excepts:
            temp = defaultdict(set)
            for exp in excepts:
                endpoint, stack_name = exp.split("::")
                temp[int(endpoint)].add(stack_name)
            for group, content in temp.items():
                total = deepcopy(self.compose_infos)
                result[group] = [i for i in total if i.stack_name not in content]
        return result

    def do_main(self) -> None:
        """入口程序."""
        base_url = self.config["base_url"]
        log_level = self.config["log_level"]
        username = self.config["username"]
        password = self.config["password"]
        endpoints = self.config["endpoints"]
        suffix = self.config["suffix"]
        cwd = self.config["cwd"]
        excepts = self.config.get("excepts")
        prune = self.config.get("prune")
        repository_url = self.config.get("repository_url")
        repository_reference_name = self.config.get("repository_reference_name")
        repository_username = self.config.get("repository_username")
        repository_password = self.config.get("repository_password")
        retry_max_times = self.config.get("retry_max_times")
        retry_interval_backoff_factor = self.config.get("retry_interval_backoff_factor")
        rq = requests.Session()
        if retry_max_times and int(retry_max_times) > 0:
            rq.mount('https://', HTTPAdapter(max_retries=Retry(total=int(retry_max_times), backoff_factor=retry_interval_backoff_factor, method_whitelist=frozenset(['GET', 'POST', 'PUT']))))
        # 初始化log
        log.initialize_for_app(app_name="UpdateStack", log_level=log_level)
        log.info("get config", config=self.config)
        # 找到所有符合条件的stack
        cwdp = Path(cwd)
        root = Path(".")
        self.find_compose(cwd=cwdp, suffix=suffix, root=root)
        # 处理excepts
        endpoints_stacks = self.handdler_excepts(excepts)
        log.debug("deal with excepts ok", endpoints_stacks=endpoints_stacks)
        # 获取jwt
        jwt = get_jwt(rq, base_url=base_url, username=username, password=password)
        log.debug("deal with jwt ok", jwt=jwt)
        # 获取已经存在的stack信息
        endpoint_stack_info = get_all_stacks_from_portainer(rq, base_url=base_url, jwt=jwt)
        log.debug("deal with endpoint_stack_info ok", endpoint_stack_info=endpoint_stack_info)
        # 获取endpoint信息
        for endpoint in endpoints:
            swarmID: Optional[str] = None
            try:
                swarmID = get_swarm_id(rq, base_url=base_url, jwt=jwt, endpoint=endpoint)
            except NotSwarmEndpointError:
                log.info("Endpoint not swarm", endpoint=endpoint)
            except Exception as e:
                raise e
            log.debug("deal with swarmID ok", swarmID=swarmID, endpoint=endpoint)
            exist_stacks = endpoint_stack_info.get(endpoint)
            if exist_stacks is None:
                continue
            preparing_stacks = endpoints_stacks[endpoint]
            for _stack in preparing_stacks:
                stack = exist_stacks.get(_stack.stack_name)
                if stack:
                    if stack.repositoryURL == repository_url and stack.repositoryReferenceName == repository_reference_name and stack.composeFilePathInRepository == _stack.path and stack.swarm_id == swarmID:
                        stack.update_or_create(rq, base_url=base_url, jwt=jwt, prune=prune,
                                               repositoryUsername=repository_username, repositoryPassword=repository_password)
                else:
                    stack = GitStackInfo(
                        endpoint_id=endpoint,
                        stack_name=_stack.stack_name,
                        swarm_id=swarmID,
                        composeFilePathInRepository=_stack.path,
                        repositoryReferenceName=repository_reference_name,
                        repositoryURL=repository_url, env=[])
                    stack.update_or_create(rq, base_url=base_url, jwt=jwt, prune=prune,
                                           repositoryUsername=repository_username, repositoryPassword=repository_password)


def get_swarm_id(rq: requests.Session, base_url: str, jwt: str, endpoint: int) -> str:
    """获取端点的SwarmID.

    Args:
        rq (requests.Session): 请求会话
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
                 headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}))
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


def get_all_stacks_from_portainer(rq: requests.Session, base_url: str, jwt: str) -> Dict[int, Dict[str, GitStackInfo]]:
    """

    Args:
        rq (requests.Session): 请求会话
        base_url (str): portainer的根地址
        jwt (str): 访问jwt

    Raises:
        HttpCodeError: get stack query get error
        e: get stack query get json result error

    Returns:
        Dict[int, Dict[str, GitStackInfo]]: dict[endpointid,dict[stack_name,stackinfo]]
    """
    res = rq.get(f"{base_url}/api/stacks",
                 headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}))
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
