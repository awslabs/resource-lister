import importlib
from resource_lister.boto_formatter.service_config_mgr.service_config import ServiceConfig
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

def process_rl_api(accounts, service_name, function_name, attributes, regions=None):
    print("Processing rl api....Please wait .... ")
    process_config = dict()
    process_config["accounts"] = accounts
    process_config["service_name"] = service_name
    process_config.update(ServiceConfig.get_service_function_details(service_name,function_name))
    process_config["attributes"] = attributes
    if regions is not None:
        process_config["regions"] = regions

    module_name = "resource_lister.processor.{}".format(
        process_config["implclass"])
    module = importlib.import_module(module_name)
    return getattr(module, process_config["implfunction"])(process_config)




