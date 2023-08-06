import os
from typing import Dict, Optional

from ucloud.client import Client

from quant_friend.api import HostIdentifier

ucloud_config: Optional[Dict] = None


def register(parameters: Optional[Dict[str, any]] = None):
    global ucloud_config

    if ucloud_config:
        if parameters:
            # 重新注册，可能需要覆盖
            ucloud_config.update(parameters)
    else:
        # 读取环境，再综合
        config = dict()
        for name in filter(lambda it: it.startswith("uc_"), iter(os.environ)):
            key = name[3:]
            config[key] = os.environ[name]
        if parameters:
            config.update(parameters)
        ucloud_config = config


def to_host_id(x):
    return HostIdentifier(x['UHostId'], "ucloud")


def create_client():
    register()
    return Client(ucloud_config)


def uc_delete_host(host: HostIdentifier):
    client = create_client()
    client.uhost().stop_uhost_instance({"UHostId": host.identifier})
    client.uhost().terminate_uhost_instance({"UHostId": host.identifier})


def uc_list_host(parameters: Dict[str, any]):
    client = create_client()

    # TotalCount 暂时不管，也不管排序
    # https://docs.ucloud.cn/api/uhost-api/describe_uhost_instance

    return list(map(to_host_id, client.uhost().describe_uhost_instance(parameters)['UHostSet']))
