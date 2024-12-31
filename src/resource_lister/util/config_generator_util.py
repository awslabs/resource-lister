
import json
import os
import logging
import resource_lister.boto_formatter.json_util.json_util as json_util
import resource_lister.util.menu_util as menu_util
import resource_lister.util.menu_configs as config_menu_configs
from resource_lister.boto_formatter.service_config_mgr.service_config import ServiceConfig
# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def process_config_files():
    input_json = dict()
    input_json_value = menu_util.process_inputs(config_menu_configs.config_generator_util_config, input_json)
    input_dir_path = input_json_value["input_dir_path"].strip()
    output_dir_path = input_json_value["output_dir_path"].strip()
    try:
        print("[START] : Processing config files ....")
        service_names = [x for x in os.listdir(input_dir_path)]
        for service_name in service_names:
            generate_config_files(service_name, input_dir_path, output_dir_path)
        print("[END] : Processing config files ....")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def upload_config_file():
    input_json = dict()
    input_json_value = menu_util.process_inputs(config_menu_configs.config_generator_upload_service_config, input_json)
    input_file_path = input_json_value["input_file_path"].strip()
    try:
        print(f"[START] : Uploading config file {input_file_path} ....")
        with open(input_file_path) as f:
            json_data = json.load(f)
            ServiceConfig.add_service_config(json_data)

        print(f"[END] : Uploaded Service config file {input_file_path} ....")
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")



# def get_service_name(file_name):
#     """
#     String assumption is file is in only in .json format
#     """
#     return file_name[0:len(file_name)-5]

def generate_config_files(service_name, input_directory, output_directory):
    """
    Iterate through all the files and flatten the JSON
    """ 
    service_dict = {}
    service_dict["service_name"] = service_name
    service_dict["functions"] = []
    logger.info(service_name)
    logger.info(input_directory)
    logger.info(output_directory)

    try:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        input_dir_path_service = os.path.join(dir_path, input_directory, service_name)
        out_dir_path_service = os.path.join(dir_path, output_directory)
        output_file = "{}.json".format(service_name)
        output_file_path = os.path.join(out_dir_path_service, output_file)
        for service_file in os.listdir(input_dir_path_service):
            if service_file.split(".")[1] == "json":
                file_path = os.path.join(input_dir_path_service, service_file)
                print("file_path {}".format(file_path))
                f = open(file_path)
                temp_data = json.load(f)
                if temp_data["service_name"] == service_name:
                    temp_data["json_response"] = json_util.flatten_json(temp_data["json_response"])
                    del temp_data["service_name"]
                    service_dict["functions"].append(temp_data)
        json_object = json.dumps(service_dict, indent=4)
        with open(output_file_path, "w") as outfile:
            outfile.write(json_object)
    except KeyError as err:
        print("Please check uploaded <service_name>.json file . File syntax is not correct.")
        raise err
    except FileNotFoundError as err:
        print(
            "File service_config.json file is not Found. Please check aws_account_config.json file exists")
        raise err
    except IOError as err:
        print(
            " IO error while loading the file aws_account_config.json {}. ".format(err))
        raise err


