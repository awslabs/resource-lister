
import os
import logging
import json
from resource_lister.session_mgr.iam_session_mgr import AccountConfig
from resource_lister.session_mgr.iam_session_mgr import Region
import resource_lister.config_mgr.config_util as config_util
from resource_lister.boto_formatter.service_config_mgr.service_config import ServiceConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


OUTPUT_DIVIDER = '''
*******************************************************************************
'''

DISCLAIMER = '''
DISCLAIMER : \n
This is experimental NO CODE Python Intractive Utility to list AWS resources activities.
To generate the list of AWS Resources Utility will make boto3  List API calls on configured accounts.These API calls will applied to your API Account Quota
If destination of output as set S3 , Utility will upload generated result on S3 bucket .
'''

def print_line():
    print("************************************************************************")


def print_disclaimer():
    print(DISCLAIMER)


class MenuData():
    __service_list = None
    __account_list = None
    __region_list = None
    __attributes = None

    @classmethod
    def load_data(cls):
        """ Load config values from menu_config.json"""
        logger.debug("loading Data for menu_config {}...")
        try:
            MenuData.__service_list  = ServiceConfig.get_services_names()
            MenuData.__account_list = AccountConfig.get_account_list()
            MenuData.__region_list = Region.get_regions()
            MenuData.__attributes = config_util.ConfigAttributes.get_config_attributes()

        except FileNotFoundError as err:
            logger.error(
                "File menu_config.json file is not Found. Please check menu_config.json file exists")
            raise err
    @classmethod
    def validate_service_name(cls, selected_service_name):
        """
        This function accept the service_name and get the function details
        """
        is_valid_service = False
        if MenuData.__service_list is None:
            MenuData.load_data()
        if selected_service_name is not None:
            service_list = MenuData.get_service_list()
            if selected_service_name in service_list:
                is_valid_service = True
            else:
                # if user types in service id
                if selected_service_name.isdigit():
                    selected_service_index = int(selected_service_name)-1
                    if selected_service_index < len(service_list):
                        is_valid_service = True
                        selected_service_name = service_list[selected_service_index]
        return is_valid_service,selected_service_name
    @classmethod
    def get_service_functions(cls, selected_service_name):
        return ServiceConfig.get_service_functions(selected_service_name)

    @classmethod
    def get_account_list(cls):
        if MenuData.__account_list is None:
            MenuData.load_data()
        return MenuData.__account_list

    @classmethod
    def get_region_list(cls):
        if MenuData.__region_list is None:
            MenuData.load_data()
        return MenuData.__region_list

    @classmethod
    def get_service_list(cls):
        if MenuData.__service_list is None:
            MenuData.load_data()
        return MenuData.__service_list

    @classmethod
    def load_attributes(cls):
        config_util.ConfigAttributes.load_config_attributes()
        MenuData.__attributes = config_util.ConfigAttributes.get_config_attributes()

    @classmethod
    def set_attributes(cls, attributes):
        MenuData.load_attributes()

    @classmethod
    def get_attributes(cls):
        if MenuData.__attributes is None:
            MenuData.load_attributes()
        return dict(MenuData.__attributes)


def print_functions(service_function_list, selected_service_name):
    count = 1
    print("Service selected [{}]:".format(selected_service_name))
    print("Please select any of following options:")
    for function_json in service_function_list:
        print("{}. {}[{}]".format(
            count, function_json["function_name"],function_json["function_description"]))
        count += 1


def print_accounts():
    count = 1
    for account in MenuData.get_account_list():
        print("{}.{}".format(count, account))
        count += 1


def print_regions():
    count = 1
    for region in MenuData.get_region_list():
        print("{}.{}".format(count, region))
        count += 1


def print_services():
    count = 1
    for service in MenuData.get_service_list():
        print("{}.{}".format(count, service))
        count += 1


def print_all_services_menu():
    count = 1
    for service in MenuData.get_service_list():
        service_function_list = MenuData.get_service_functions(service)
        for function_json in service_function_list:
            print("{},{},{},{}".format(count, service,
                  function_json["function_name"], function_json["function_description"]))
            count += 1

# print_menu_data(MenuData().search_menu_data("lambda"))
