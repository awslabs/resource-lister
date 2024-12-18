import resource_lister.processor.core_processor_api as core_processor_api
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

class RLApi():
    __services_names = []
    @classmethod
    def get_list_of_services(cls) -> list:
        if len(RLApi.__services_names) ==0:
            RLApi.__services_names= ServiceConfig.get_services_names()
        return RLApi.__services_names

    @classmethod
    def get_service_function_names(self,service_name) ->list:
        try:
                return ServiceConfig.get_function_names(service_name)
        except IndexError as err:
            ERROR_MESSAGE = " {} Option is invalid , Please select function ".format(service_name)
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        except ValueError as err:
            ERROR_MESSAGE = " {} Option is invalid , Please select function ".format(service_name)
            #logger.error(err)
            raise ValueError("Invalid  service selected {}. Please choose a service from the options : {}".format(service_name,ServiceConfig.get_services_names()))

    @classmethod
    def get_service_function_details(self,service_name,function_name):
        try:
                return ServiceConfig.get_service_function_details(service_name,function_name)
        except IndexError as err:
            ERROR_MESSAGE = " {} Option is invalid , Please select function ".format(service_name)
            logger.error(err)
            raise ValueError(ERROR_MESSAGE)
        except ValueError as err:
            ERROR_MESSAGE = " {} Option is invalid , Please select function ".format(service_name)
            #logger.error(err)
            raise ValueError("Invalid  service selected {}. Please choose a service from the options : {}".format(service_name,ServiceConfig.get_services_names()))
        
    def get_resource_list(self,service_name, function_name, accounts)->list:
        attributes = {
            "format_type": "csv",
            "required": "no",
            "account_split": "no",
            "s3_bucket": "",
            "file_append_date": "no",
            "output_to":"none"
        }  
        return core_processor_api.process_rl_api(accounts, service_name, function_name, attributes) 