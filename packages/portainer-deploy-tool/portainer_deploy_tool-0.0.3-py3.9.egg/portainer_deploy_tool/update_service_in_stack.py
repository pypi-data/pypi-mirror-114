from typing import Dict, Any, List, Optional
import yaml
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from schema_entry import EntryPoint
from pyloggerhelper import log
from .utils import base_schema_properties, get_jwt, HttpCodeError


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
    "registry_name": {
        "type": "string",
        "title": "n",
        "description": "镜像仓库名",
    },
    "artifact_name": {
        "type": "string",
        "title": "n",
        "description": "要更新的镜像名",
    },
    "artifact_version": {
        "type": "string",
        "title": "v",
        "description": "要更新的镜像版本",
        "default": "latest"
    },
    "tag_prefix": {
        "type": "string",
        "title": "t",
        "description": "待更新路径"
    },
    "deploy_path": {
        "type": "array",
        "items": {
            "type": "string"
        },
        "title": "d",
        "description": "待更新路径,形式为`[ENDPOINT_ID]/[STACK_ID]/[SERVICE_NAME]`"
    }
}

schema_properties.update(**base_schema_properties)


class UpdateServiceInStack(EntryPoint):
    """更新已经存在的stack."""
    default_config_file_paths = [
        "./update_service_in_stack_config.json"
    ]
    argparse_noflag = "deploy_path"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["base_url", "username", "password", "artifact_name", "artifact_version", "deploy_path"],
        "properties": schema_properties
    }

    def parser_deploy_path(self, deploy_path: List[str]) -> Dict[str, List[str]]:
        """解析deploy_path便于部署.

        Args:
            deploy_path (List[str]): 待更新路径,形式为`[ENDPOINT_ID]/[STACK_ID]/[SERVICE_NAME],[ENDPOINT_ID]/[STACK_ID]/[SERVICE_NAME]...`

        Raises:
            AttributeError: stack_id must be digit
            AttributeError: endpoint_id must be digit

        Returns:
            Dict[str, List[str]]: key为<endpoint_id_str>::<stack_id>;value为其中要更新的service名称列表
        """
        services: Dict[str, List[str]] = {}
        for p in deploy_path:
            endpoint_id, stack_id, service_name = p.split("/")
            if not stack_id.isdigit():
                log.error("stack_id must be digit", stack_id=stack_id)
                raise AttributeError(f"stack_id must be digit, but is {stack_id}")
            if not endpoint_id.isdigit():
                log.error("endpoint_id must be digit", endpoint_id=endpoint_id)
                raise AttributeError(f"endpoint_id must be digit, but is{endpoint_id}")

            stack_key = f"{endpoint_id}::{stack_id}"
            if services.get(stack_key):
                services[stack_key].append(service_name)
            else:
                services[stack_key] = [service_name]
        return services

    def make_image_name(self, artifact_name: str, artifact_version: str, *,
                        registry_name: Optional[str] = None, tag_prefix: Optional[str] = None) -> str:
        """[summary]

        Args:
            artifact_name (str): 制品名
            artifact_version (str): 制品版本
            registry_name (Optional[str], optional): 镜像仓库hostname. Defaults to None.
            tag_prefix (Optional[str], optional): 制品版本标签前缀. Defaults to None.

        Returns:
            str: 完整镜像名
        """
        if registry_name:
            if tag_prefix:
                image_name = f"{registry_name}/{artifact_name}:{tag_prefix}-{artifact_version}"
            else:
                image_name = f"{registry_name}/{artifact_name}:{artifact_version}"
        else:
            if tag_prefix:
                image_name = f"{artifact_name}:{tag_prefix}-{artifact_version}"
            else:
                image_name = f"{artifact_name}:{artifact_version}"
        return image_name

    def get_stack_file_content(self, rq: requests.Session, base_url: str, jwt: str, stack_id: str) -> str:
        """获取更新前stack的compose文本.

        Args:
            rq (requests.Session): 请求会话
            base_url (str): portainer基础路径
            jwt (str): 访问jwt
            stack_id (str): stack信息的id

        Raises:
            HttpCodeError: get stack file content query get error
            e: get stack file content query get json result error
            AttributeError: get stack file content query has no field StackFileContent

        Returns:
            str: 旧compose文本
        """
        res = rq.get(
            f"{base_url}/stacks/{stack_id}/file",
            headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt})
        )
        if res.status_code != 200:
            log.error("get stack file content query get error", stack_id=stack_id, status_code=res.status_code)
            raise HttpCodeError("get stack file content query get error")
        try:
            res_json = res.json()
        except Exception as e:
            log.error("get stack file content query get json result error", stack_id=stack_id, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
            raise e
        else:
            StackFileContent = res_json.get("StackFileContent")
            if StackFileContent:
                return StackFileContent
            else:
                log.error("get stack file content query has no field StackFileContent", stack_id=stack_id)
                raise AttributeError("get stack file content query has no field StackFileContent")

    def deploy(self, rq: requests.Session, base_url: str, jwt: str, image_name: str, stack_key: str, services: List[str]) -> None:
        """更新部署单个stack中的服务.

        Args:
            rq (requests.Session): 请求会话
            base_url (str): portainer基础路径
            jwt (str): 访问jwt
            image_name (str): 镜像完整名
            stack_key (str): stack信息,形式为<endpoint_id_str>::<stack_id>
            services (List[str]): 这个stack中要更新的services名称列表

        Raises:
            HttpCodeError: service_name not in old compose file
            AttributeError: deploy query get error
            e: deploy query get json result error
        """
        endpoint_id_str, stack_id = stack_key.split("::")
        endpoint_id = int(endpoint_id_str)
        StackFileContent = self.get_stack_file_content(rq, base_url=base_url, jwt=jwt, stack_id=stack_id)
        s = yaml.load(StackFileContent)
        log.info("get old compose", content=s)
        for service_name in services:
            if s['services'].get(service_name):
                s['services'][service_name]['image'] = image_name
            else:
                log.error("service_name not in old compose file", service_name=service_name)
                raise AttributeError(f"service_name {service_name} not in old compose file")
        compose = yaml.dump(s, sort_keys=False)
        res = rq.put(
            f"{base_url}/stacks/{stack_id}",
            headers=requests.structures.CaseInsensitiveDict({"Authorization": "Bearer " + jwt}),
            params={"endpointId": endpoint_id},
            json={
                "StackFileContent": compose,
                "Prune": False
            }
        )
        if res.status_code != 200:
            log.error("deploy query get error", stack_key=stack_key, status_code=res.status_code)
            raise HttpCodeError("deploy query get error")
        else:
            try:
                res_json = res.json()
            except Exception as e:
                log.error("deploy query get json result error", stack_key=stack_key, err=type(e), err_msg=str(e), exc_info=True, stack_info=True)
                raise e
            else:
                log.debug("deploy query get result", stack_key=stack_key, cotent=res_json)
                log.info("deploy ok", stack_key=stack_key)

    def deploy_all(self, rq: requests.Session, base_url: str, jwt: str, image_name: str, stack_services: Dict[str, List[str]]) -> None:
        """部署解析出来的所有stack.

        Args:
            rq (requests.Session): 请求会话
            base_url (str): portainer基础路径
            jwt (str): 访问jwt
            image_name (str): 镜像完整名
            stack_services (List[str]): 解析出来的stack-service信息
        """
        for stack_key, services in stack_services.items():
            self.deploy(
                rq,
                base_url=base_url,
                jwt=jwt,
                image_name=image_name,
                stack_key=stack_key,
                services=services)
        log.info("deploy all done")

    def do_main(self) -> None:
        """入口程序."""
        base_url = self.config["base_url"]
        log_level = self.config["log_level"]
        username = self.config["username"]
        password = self.config["password"]
        artifact_name = self.config["artifact_name"]
        artifact_version = self.config["artifact_version"]
        deploy_path = self.config["deploy_path"]
        retry_max_times = self.config.get("retry_max_times")
        retry_interval_backoff_factor = self.config.get("retry_interval_backoff_factor")
        rq = requests.Session()
        if retry_max_times and int(retry_max_times) > 0:
            rq.mount('https://', HTTPAdapter(max_retries=Retry(total=int(retry_max_times), backoff_factor=retry_interval_backoff_factor, method_whitelist=frozenset(['GET', 'POST', 'PUT']))))
        log.initialize_for_app(app_name="UpdateStack", log_level=log_level)
        jwt = get_jwt(rq, base_url=base_url, username=username, password=password)
        image_name = self.make_image_name(
            artifact_name=artifact_name,
            artifact_version=artifact_version,
            registry_name=self.config.get("registry_name"),
            tag_prefix=self.config.get("tag_prefix")
        )
        stack_services = self.parser_deploy_path(deploy_path)
        self.deploy_all(
            rq,
            base_url=base_url,
            jwt=jwt,
            image_name=image_name,
            stack_services=stack_services
        )
