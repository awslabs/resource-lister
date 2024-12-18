import importlib


def process(process_config):
    """
    Main processing engine
    Calls implemenation function based on service configuration
    """
    print("Processing ....Please wait .... ")
    module_name = "resource_lister.processor.{}".format(
        process_config["implclass"])
    module = importlib.import_module(module_name)
    return getattr(module, process_config["implfunction"])(process_config)
