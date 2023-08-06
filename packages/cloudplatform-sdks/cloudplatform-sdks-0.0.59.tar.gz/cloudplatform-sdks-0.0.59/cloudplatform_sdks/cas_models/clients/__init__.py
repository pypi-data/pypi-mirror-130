import importlib
from proxy_tools import proxy
from .ecs_client import CASEcsClient

prod_mapper = {
    'ecs': CASEcsClient,
}


def get_current_client(prod):
    module = importlib.import_module('cloudplatform_auth')
    get_access_func = getattr(module, 'get_cas_access_info')
    connection_config = get_access_func()
    username, password, url = connection_config.get("username"), connection_config.get("password"), \
                              connection_config.get("url")
    return prod_mapper[prod](username, password, url)


@proxy
def cas_ecs_client():
    return get_current_client('ecs')


