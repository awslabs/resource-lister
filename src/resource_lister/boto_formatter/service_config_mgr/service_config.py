"""
Read all the service definations from service_configs and store the values
in dictionary.

"""
import logging
import os
import json

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def get_service_name(file_name):
    """
    File should be in .json format
    This function strip last four character .json and return value
    :param file_name
    :return: service_name
    """
    json_file_name = None
    try:
        file_len = len(file_name)
        if file_name[file_len-5:file_len] ==".json":
                json_file_name = file_name[0:len(file_name)-5]
                  
    except Exception as err:
        logger.error(err)
        ERROR_MESSAGE = " Invalid file {} found in service_config directory. service_config shoudl contain only .json files".format(
            file_name)
        raise ValueError(ERROR_MESSAGE)

    return json_file_name


class ServiceConfig():
    """ This class hold the  values from service_configs"""
    __data = {}
    __service_functions_dict= dict()
    __services_names= []

    @classmethod
    def load_all_service_data(cls):
        """ Load config values for all services"""
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            dir_path_service = os.path.join(dir_path, "service_configs")
            for service_file in os.listdir(dir_path_service):
                service_name = get_service_name(service_file)
                if service_name:
                    logger.info("{}.json found ".format(service_name))
                    file_path = os.path.join(dir_path_service, service_file)
                    f = open(file_path)
                    temp_data = json.load(f)
                    service_name = temp_data["service_name"]
                    ServiceConfig.__data[service_name] = {}
                    
                    ServiceConfig.__data[service_name]["service_name"] = service_name
                    service_functions_list =[]
                    for function_details in temp_data["functions"]:
                        function_name = function_details["function_name"]
                        #print("Funciton Name {} ".format(function_name))
                        processed_function_details = ServiceConfig.__process_function_details(
                            function_details)
                        service_functions_list.append(processed_function_details)
                        ServiceConfig.__data[service_name][function_name] = processed_function_details
                    ServiceConfig.__service_functions_dict[service_name]=service_functions_list
                    #print(ServiceConfig.__services_function_dict)
                    f.close()
                else:
                    logger.info(" Invalid file {} found ".format(service_name))
            # Populate seperate list for service names
            __services_names = list(ServiceConfig.__service_functions_dict.keys())
            __services_names.sort()
            ServiceConfig.__services_names = __services_names
            #print(ServiceConfig.__services_names)
        except KeyError as err:
            logger.error(
                "Please check service_config.json file . File syntax is not correct.")
            raise err
        except FileNotFoundError as err:
            logger.error(
                "File service_config.json file is not Found. Please check aws_account_config.json file exists")
            raise err
        except IOError as err:
            logger.error(
                " IO error while loading the file aws_account_config.json {}. ".format(err))
            raise err

    # @classmethod
    # def load_service_data(cls, service_name):
    #     """ Load config values for perticular service from <service_name>.json file in service_configs folder"""
    #     logger.info("loading Data for service_name {}...".format(service_name))
    #     try:
    #         dir_path = os.path.dirname(os.path.abspath(__file__))
    #         dir_path_service = os.path.join(dir_path, "service_configs")
    #         for service_file in os.listdir(dir_path_service):
    #             if service_name == get_service_name(service_file):
    #                 file_path = os.path.join(dir_path_service, service_file)
    #                 f = open(file_path)
    #                 temp_data = json.load(f)
    #                 service_name = temp_data["service_name"]
    #                 ServiceConfig.__data[service_name] = {}
    #                 ServiceConfig.__data[service_name]["service_name"] = service_name
    #                 for function_details in temp_data["functions"]:
    #                     function_name = function_details["function_name"]
    #                     ServiceConfig.__data[service_name][function_name] = ServiceConfig.__process_function_details(
    #                         function_details)
    #                 f.close()
    #     except KeyError as err:
    #         logger.error(
    #             "Please check service_config.json file . File syntax is not correct.")
    #         raise err
    #     except FileNotFoundError as err:
    #         logger.error(
    #             "File service_config.json file is not Found. Please check aws_account_config.json file exists")
    #         raise err
    #     except IOError as err:
    #         logger.error(
    #             " IO error while loading the file aws_account_config.json {}. ".format(err))
    #         raise err

    @classmethod
    def get_service_function_details(cls, service_name, function_name)->dict:
        """ returns perticular function configuration"""
        fucntion_config = {}
        try:
            if len(ServiceConfig.__data.keys())==0:
                ServiceConfig.load_all_service_data()
            fucntion_config = ServiceConfig.__data[service_name][function_name]
        except KeyError as err:
            ERROR_MESSAGE = " Either Service config  {}.json not found in service_configs folder or function {} is not defined in {}.json".format(
                service_name, function_name, service_name)
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        return fucntion_config
    


    @classmethod
    def get_services_names(cls)->list:
        """ returns string of configured services"""
        try:
            if len(ServiceConfig.__data.keys())==0:
                ServiceConfig.load_all_service_data()  
        except KeyError as err:
            ERROR_MESSAGE = " Service config  {}.json not found "
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        return ServiceConfig.__services_names
    
    @classmethod
    def get_service_functions(cls,service_name) ->list:
        """ returns list of dictionary of function configurations for provided service"""
        function_names =None
        try:
            if len(ServiceConfig.__data.keys())==0:
                ServiceConfig.load_all_service_data()
            function_names= ServiceConfig.__service_functions_dict[service_name]
              
        except KeyError as err:
            ERROR_MESSAGE = " Service config  {}.json not found ".format(service_name)
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        return function_names
   

    @classmethod
    def __process_function_details(cls, function_details):
        """ Add required only json_response """
        json_response_required = dict()
        json_response = function_details["json_response"]
        for key in json_response.keys():
            if json_response[key] == "required":
                json_response_required[key] = json_response[key]
        function_details["json_response_required"] = json_response_required
        return function_details
    
