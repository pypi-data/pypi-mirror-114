from typing import Dict, Any
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from schema_entry import EntryPoint
from pyloggerhelper import log
from .utils import base_schema_properties, HttpCodeError


schema_properties: Dict[str, Any] = {
    "tokens": {
        "type": "array",
        "items": {
            "type": "string"
        },
        "title": "o",
        "description": "webhook的token"
    },
}

schema_properties.update(**base_schema_properties)


class UpdateServiceByWebhooks(EntryPoint):
    """利用webhook更新已经存在的service."""
    default_config_file_paths = [
        "./update_service_by_webhooks_config.json"
    ]
    argparse_noflag = "tokens"
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": ["base_url", "tokens"],
        "properties": schema_properties
    }

    def do_main(self) -> None:
        """入口程序."""
        base_url = self.config["base_url"]
        log_level = self.config["log_level"]
        tokens = self.config["tokens"]
        retry_max_times = self.config.get("retry_max_times")
        retry_interval_backoff_factor = self.config.get("retry_interval_backoff_factor", 0)
        rq = requests.Session()
        if retry_max_times and int(retry_max_times) > 0:
            rq.mount('https://', HTTPAdapter(max_retries=Retry(total=int(retry_max_times), backoff_factor=retry_interval_backoff_factor, method_whitelist=frozenset(['GET', 'POST', 'PUT']))))
        log.initialize_for_app(app_name="UpdateStack", log_level=log_level)
        for token in tokens:
            res = rq.post(f"{base_url}/api/webhooks/{token}")
            if res.status_code >= 300 or res.status_code <= 199:
                log.error("update service query get error", status_code=res.status_code)
            else:
                log.info("update service query ok", status_code=res.status_code)
