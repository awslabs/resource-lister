"""
This is supporting functions to for batch processing option
"""
import logging
import resource_lister.menu.menu_util as menu_util
import resource_lister.processor.core_processor as core_processor
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def process_batch():
    # Get list of configured accounts
    account_list = menu_util.MenuData.get_account_list()
    account_selected = None
    is_account_validated = False
    no_process_break = True
    while not is_account_validated:
        account_selected_input = input("Please enter account id  HERE--> ").strip()
        # When user selects -1 break the loop
        if account_selected == "-1":
            no_process_break = False
            break
        else:
            # if account is valid
            if account_selected_input in account_list:
                account_selected = account_selected_input
                is_account_validated = True
            else:
                print("Please enter valid accounts : Valid accounts are .. ")
                menu_util.print_accounts()
    if no_process_break:
        if account_selected:
            process(account_selected)


# def process_old(account_selected):
#     """
#     1. Get configuration information for each menu (menu_config.json)
#     2. Process only those services who are qualifed for multi account support
#     3. Process only those services who doesn't require any user input 
#     """

#     count = 1
#     region_list = menu_util.MenuData.get_region_list()
#     account_list = []
#     account_list.append(account_selected)
#     begin_time = time.time()
#     pagination_attribute_flag = True
#     attributes = menu_util.MenuData.get_attributes()
#     attributes["is_batch"] = "True"
#     for service in menu_util.MenuData.get_service_list():
#         menu_list = menu_util.MenuData().search_menu_data(service)
#         for process_config in menu_list:
#             process_config_obj = dict(process_config)
#             pagination_attribute_flag = True
#             if process_config_obj["is_multi_account_support"] == "yes":
#                 start_time = time.time()
#                 process_config_obj["accounts"] = account_list
#                 if process_config_obj["is_regional"] == "yes":
#                     process_config_obj["regions"] = region_list
#                 if "pagination_attributes" in process_config_obj.keys():
#                     refined_pagination_attributes = {}
#                     for pagination_attribute in process_config_obj["pagination_attributes"]:
#                         if pagination_attribute["is_visible"].upper() == "YES":
#                             pagination_attribute_flag = False
#                         else:
#                             refined_pagination_attributes[pagination_attribute["attribute_name"]
#                                                           ] = pagination_attribute["attribute_value"]
#                             process_config_obj["pagination_attributes"] = refined_pagination_attributes
#                 process_config_obj["attributes"] = dict(attributes)
#                 if pagination_attribute_flag:
#                     print("Start Processing for service : {} function :{}".format(process_config_obj["service_name"],process_config_obj["function_name"]))
#                     # core processor process the service
#                     core_processor.process(process_config_obj)
#                     print("Report generated for service {} function {} :TIME Taken -->{}".format(
#                         process_config_obj["service_name"], process_config_obj["function_name"], (time.time() - start_time)))
#                     count += 1
#     print("Batch completed : Number of functions  --> {} ".format(count))
#     print("Batch completed : Took TIME --> {} ".format((time.time() - begin_time)))


def process(account_selected):
    """
    1. Get configuration information for each menu (menu_config.json)
    2. Process only those services who are qualifed for multi account support
    3. Process only those services who doesn't require any user input 
    """

    count = 1
    region_list = menu_util.MenuData.get_region_list()
    account_list = []
    account_list.append(account_selected)
    begin_time = time.time()
    pagination_attribute_flag = True
    attributes = menu_util.MenuData.get_attributes()
    attributes["is_batch"] = "True"
    for service in menu_util.MenuData.get_service_list():
        service_functions = menu_util.MenuData().get_service_functions(service)
        for function_config in service_functions:

            function_config_obj = dict(function_config)
            if "no_batch_support" not in function_config_obj.keys():
                function_config_obj["service_name"] = service
                pagination_attribute_flag = True
                if function_config_obj["is_multi_account_support"] == "Y":
                    start_time = time.time()
                    function_config_obj["accounts"] = account_list
                    if function_config_obj["is_regional"] == "Y":
                        function_config_obj["regions"] = region_list
                    if "pagination_attributes" in function_config_obj.keys():
                        refined_pagination_attributes = {}
                        for pagination_attribute in function_config_obj["pagination_attributes"]:
                            if pagination_attribute["is_visible"].upper() == "Y":
                                pagination_attribute_flag = False
                            else:
                                refined_pagination_attributes[pagination_attribute["attribute_name"]
                                                            ] = pagination_attribute["attribute_value"]
                                function_config_obj["pagination_attributes"] = refined_pagination_attributes
                    function_config_obj["attributes"] = dict(attributes)
                    if pagination_attribute_flag:
                        print("Start Processing for service : {} function :{}".format(function_config_obj["service_name"],function_config_obj["function_name"]))
                        # core processor process the service
                        core_processor.process(function_config_obj)
                        print("Report generated for service {} function {} :TIME Taken -->{}".format(
                            function_config_obj["service_name"], function_config_obj["function_name"], (time.time() - start_time)))
                        count += 1
    print("Batch completed : Number of functions  --> {} ".format(count))
    print("Batch completed : Took TIME --> {} ".format((time.time() - begin_time)))


