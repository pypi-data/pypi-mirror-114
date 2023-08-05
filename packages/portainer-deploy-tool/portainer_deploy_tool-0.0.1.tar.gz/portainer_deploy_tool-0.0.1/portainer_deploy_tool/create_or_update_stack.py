from pathlib import Path
from copy import deepcopy
from collections import defaultdict
from typing import Dict, Any, List, NamedTuple, DefaultDict, Optional
import requests as rq
from schema_entry import EntryPoint
from pyloggerhelper import log
from .utils import (
    GitStackInfo,
    base_schema_properties,
    get_jwt,
    get_swarm_id,
    get_all_stacks_from_portainer,
    NotSwarmEndpointError
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
    },
    "retry_max_times": {
        "type": "integer",
        "description": "重试次数",
    },
    "retry_interval": {
        "type": "number",
        "description": "重试间隔时间",
        "default": 3
    }
}

schema_properties.update(**base_schema_properties)


class ComposeInfo(NamedTuple):
    stack_name: str
    path: str


class CreateOrUpdateStack(EntryPoint):
    """扫描指定目录下的compose文件,在指定的端点中如果已经部署则更新stack,否则创建stack."""
    default_config_file_paths = [
        "./create_or_update_stack_config.json"
    ]
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
        retry_interval = self.config.get("retry_interval")
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
        jwt = get_jwt(base_url=base_url, username=username, password=password)
        log.debug("deal with jwt ok", jwt=jwt)
        # 获取已经存在的stack信息
        endpoint_stack_info = get_all_stacks_from_portainer(base_url=base_url, jwt=jwt)
        log.debug("deal with endpoint_stack_info ok", endpoint_stack_info=endpoint_stack_info)
        # 获取endpoint信息
        for endpoint in endpoints:
            swarmID: Optional[str] = None
            try:
                swarmID = get_swarm_id(base_url=base_url, jwt=jwt, endpoint=endpoint)
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
                        stack.update_or_create(base_url=base_url, jwt=jwt, prune=prune,
                                               repositoryUsername=repository_username, repositoryPassword=repository_password,
                                               retry_max_times=retry_max_times, retry_interval=retry_interval)
                else:
                    stack = GitStackInfo(
                        endpoint_id=endpoint,
                        stack_name=_stack.stack_name,
                        swarm_id=swarmID,
                        composeFilePathInRepository=_stack.path,
                        repositoryReferenceName=repository_reference_name,
                        repositoryURL=repository_url, env=[])
                    stack.update_or_create(
                        base_url=base_url, jwt=jwt, prune=prune,
                        repositoryUsername=repository_username, repositoryPassword=repository_password,
                        retry_max_times=retry_max_times, retry_interval=retry_interval)
