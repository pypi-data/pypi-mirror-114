from typing import Dict, Any, Optional
import requests as rq
from schema_entry import EntryPoint
from pyloggerhelper import log
from .utils import base_schema_properties


schema_properties: Dict[str, Any] = {
    "token": {
        "type": "string",
        "title": "o",
        "description": "webhook的token"
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
    }
}

schema_properties.update(**base_schema_properties)


class UpdateServiceByWebhooks(EntryPoint):
    """利用webhook更新已经存在的service."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["base_url", "token"],
        "properties": schema_properties
    }

    def make_tag_name(self, artifact_version: str, *, tag_prefix: Optional[str] = None) -> str:
        """构造service要更新的tag.

        Args:
            artifact_version (str): 制品版本
            tag_prefix (Optional[str], optional): 制品版本标签前缀. Defaults to None.

        Returns:
            str: 完整tag名
        """
        if tag_prefix:
            tag_name = f"{tag_prefix}-{artifact_version}"
        else:
            tag_name = f"{artifact_version}"

        return tag_name

    def do_main(self) -> None:
        """入口程序."""
        base_url = self.config["base_url"]
        log_level = self.config["log_level"]
        token = self.config["token"]
        log.initialize_for_app(app_name="UpdateStack", log_level=log_level)
        if self.config.get("artifact_version"):
            tag = self.make_tag_name(artifact_version=self.config.get("artifact_version"), tag_prefix=self.config.get("tag_prefix"))
            res = rq.post(f"{base_url}/webhooks/{token}?tag={tag}")
        else:
            res = rq.post(f"{base_url}/webhooks/{token}")
        if res.status_code >= 300 or res.status_code <= 199:
            log.error("update service query get error", status_code=res.status_code)
        else:
            log.info("update service query ok", status_code=res.status_code)
