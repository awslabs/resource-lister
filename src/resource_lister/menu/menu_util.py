
import os
import logging
import json
from resource_lister.session_mgr.iam_session_mgr import AccountConfig
from resource_lister.session_mgr.iam_session_mgr import Region
import resource_lister.config_mgr.config_util as config_util

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
    __menu_data = None
    __menu_index_data = None
    __service_list = []
    __account_list = None
    __region_list = None
    __attributes = None

    @classmethod
    def load_data(cls):
        """ Load config values from menu_config.json"""
        logger.debug("loading Data for menu_config {}...")
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, "menu_config.json")
            f = open(file_path)
            temp_data = json.load(f)
            MenuData.__menu_data = temp_data["menus"]
            MenuData.__menu_index_data = {}
            # Update Menu index data and service list
            for _menu in MenuData.__menu_data:
                MenuData.__menu_index_data[_menu["menu_index"]] = _menu
                if _menu["service_name"] not in MenuData.__service_list:
                    MenuData.__service_list.append(_menu["service_name"])
            f.close()
            MenuData.__service_list.sort()
            MenuData.__account_list = AccountConfig.get_account_list()
            MenuData.__region_list = Region.get_regions()

        except FileNotFoundError as err:
            logger.error(
                "File menu_config.json file is not Found. Please check menu_config.json file exists")
            raise err

    def search_menu_data(self, menu_str):
        result = None
        if MenuData.__menu_data is None:
            MenuData.load_data()
        if menu_str is not None:
            menu_str = menu_str.strip().lower()
            service_list = MenuData.get_service_list()
            # if user types in service name
            if menu_str in service_list:
                result = []
                for _menu in MenuData.__menu_data:
                    if menu_str == _menu["service_name"]:
                        result.append(dict(_menu))
            else:
                # if user types in service id
                if menu_str.isdigit():
                    menu_item_index = int(menu_str)-1
                    if menu_item_index <= len(service_list):
                        service_name = service_list[menu_item_index]
                        result = []
                        for _menu in MenuData.__menu_data:
                            if service_name == _menu["service_name"]:
                                result.append(dict(_menu))

        return result

    @classmethod
    def get_menu_item(cls, menu_index):
        menu_item = None
        if MenuData.__menu_index_data is None:
            MenuData.load_data()
        if menu_index is None:
            raise ValueError("Please select valid option :")
        else:
            menu_index = menu_index.strip().lower()
            try:
                menu_item = dict(MenuData.__menu_index_data[menu_index])
            except KeyError as err:
                logger.error(err)
                raise ValueError("Please select valid option")

        return menu_item

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
        if len(MenuData.__service_list) == 0:
            MenuData.load_data()
        return MenuData.__service_list

    @classmethod
    def load_attributes(cls):
        MenuData.__attributes = config_util.ConfigAttributes.get_config_attributes()

    @classmethod
    def set_attributes(cls, attributes):
        MenuData.load_attributes()

    @classmethod
    def get_attributes(cls):
        if MenuData.__attributes is None:
            MenuData.load_attributes()
        return dict(MenuData.__attributes)


def print_menu_data(result, service_name):
    count = 1
    print("Service selected [{}]:".format(service_name))
    print("Please select any of following options:")
    for menu_item in result:
        print("{}. [{}]".format(
            count, menu_item["menu_help"]))
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
        menu_list = MenuData().search_menu_data(service)
        for _menu in menu_list:
            print("{},{},{},{}".format(count, service,
                  _menu["menu_index"], _menu["menu_help"]))
            count += 1

# print_menu_data(MenuData().search_menu_data("lambda"))
