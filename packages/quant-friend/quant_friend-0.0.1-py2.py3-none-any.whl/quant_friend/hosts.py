from quant_friend.api import HostIdentifier
from quant_friend.ucloud import uc_list_host, uc_delete_host


def register_ucloud(**kwargs):
    """
    注册 ucloud 服务

    即便不通过明式注册，系统也会通过读取环境变量自行注册，手动注册优先级更高。

    自动注册的规则，uc_ 开头的所有环境变量 都会被自动注册。
    举例 若环境中 存在 uc_id = 100, 那么相当于执行了 register_ucloud(id=100)
    :param kwargs:
    """
    from quant_friend.ucloud import register
    register(kwargs)


def list_and_delete_host(brand: str, **kwargs):
    """
    搜索并且干掉符合条件的主机
    关键字参数 ucloud 可参考 https://docs.ucloud.cn/api/uhost-api/describe_uhost_instance

    :param brand: ucloud or aliyun
    :param kwargs: 任意请求参数，基于不同的供应商参数并不一致
    """
    for host in list_host(brand, kwargs=kwargs):
        delete_host(host)


def delete_host(host: HostIdentifier):
    """
    删除特地主机
    :param host: 特定主机
    """
    if host.brand == "ucloud":
        uc_delete_host(host)
    pass


def list_host(brand: str, **kwargs):
    """
    关键字参数 ucloud 可参考 https://docs.ucloud.cn/api/uhost-api/describe_uhost_instance

    :param brand: ucloud or aliyun
    :param kwargs: 任意请求参数，基于不同的供应商参数并不一致
    :return: 符合的主机列表
    """
    if brand == "ucloud":
        return uc_list_host(kwargs)
