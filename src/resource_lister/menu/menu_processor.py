
import os
import sys
import logging
import resource_lister.util.setup as setup
import resource_lister.menu.menu_util as menu_util
import resource_lister.menu.batch_processing as batch_processing
import resource_lister.processor.core_processor as core_processor
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


OUTPUT_DIVIDER = '''
*******************************************************************************
'''

DISCLAIMER = '''
DISCLAIMER :
This is  NO CODE Python Intractive Utility to list AWS resources 
across AWS Accounts.
WARNING :
To generate the list of AWS Resources Utility will make boto3  List API calls 
on configured accounts.These API calls will applied to your API Account Quotas.
'''



def print_line():
    print("*******************************************************************************")

def get_menu_seperator():
    return "==============================================================================="


def get_menu_exit_seperator():
    return "-------------------------------------------------------------------------------"

def print_menu_header(menu_link):
    print(get_menu_seperator())
    print("{} :".format(menu_link))
    print(get_menu_seperator())



def print_disclaimer():
    print(DISCLAIMER)


def print_help():
    help_menu = ["1. [Manage AWS Account]", "2. [List configured AWS Accounts]",
                "3. [List AWS Regions]", "4. [List configured AWS services]","5. [List configured AWS functions]",
                "6. [Manage Configurations (example : format_type, output_type)]","7. [Batch Processing]"]
    help_menu_link = "MENU [MAIN-->HELP]"
    help_menu_question = "Select one of following options :"
    exit_menu = ["0. [Exit from HELP]", "-1.[Return to previous menu]"]
    print_menu_header(help_menu_link)
    print("{}".format(help_menu_question))
    for menu in help_menu:
        print(menu)
    for menu in exit_menu:
        print(menu)
    print("{}".format(get_menu_exit_seperator()))


def process():
    print_line()
    print_disclaimer()
    print_line()
    print_line()
    print_configure_utility()
    print_line()
    process_input()


def print_configure_utility():
    attributes = menu_util.MenuData.get_attributes()
    CONFIGURATION = "CURRENT CONFIGURATIONS :\n  Format Type (csv/json) : {} \n  Output To (print/file/s3) :{}\n  Generate only required Columns (yes/no): {}\n  Generate seperate file for each AWS Account (yes/no) : {}\n  S3 Bucket : {}\n".format(
        attributes["format_type"], attributes["output_to"], attributes["required"], attributes["account_split"], attributes["s3_bucket"])
    print(CONFIGURATION)


def process_help():
    in_process_help = True
    while in_process_help:
        print_help()
        input_value = input("Enter Option # HERE:-->")
        input_value = input_value.strip().lower()
        if input_value == "0" or input_value == "-1":
            break
        elif input_value == "1":
            print_line()
            setup.process_account_setup()
            menu_util.MenuData.load_data()
        elif input_value == "2":
            print_line()
            print("List of supported accounts ")
            menu_util.print_accounts()
            print_line()
        elif input_value == "3":
            print_line()
            print("List of regions")
            menu_util.print_regions()
            print_line()
        elif input_value == "4":
            print_line()
            print("List of supported AWS services ")
            menu_util.print_services()
            print_line()
        elif input_value == "5":
            print_line()
            print("List of supported AWS functions ")
            menu_util.print_all_services_menu()
            print_line()
        elif input_value == "6":
            print_line()
            print_configure_utility()
            setup.process_config_setup()
            menu_util.MenuData.load_attributes()
            print_line()

        elif input_value == "7":
            print_line()
            print("WARNING..  : Batch processing will go through all the services and functions configured in utility.")
            print(
                "WARNING..  : It will use boto3 API calls and in some cases service API Quotas.")
            confrm_msg = input(
                "Do you want to start the batch ?[Yes/No]:-->").strip()
            if confrm_msg.upper() == "YES":
                batch_processing.process_batch()

        else:
            print("Please enter valid option [0,1,2,3,4,5,6,7]")
    process_input()


def process_input():
    menu_option = -999
    while menu_option != 0:
        try:
            print_line()
            process_config = None
            print_menu_header("MENU [MAIN]")
            input_value = input("Enter AWS service for help (help) for Exit(0) :-->").strip().lower()
            if input_value == "help":
                process_help()
                break
            # Exit option
            elif input_value == "0":
                menu_option = 0
                break
            else:
                menu_list = menu_util.MenuData().search_menu_data(input_value)
                # if invalid service selected menu_list would be None
                if menu_list is None:
                    print("Invalid service {} selected .Please try again with any of following services".format(
                        input_value))
                    menu_util.print_services()
                    input("Please enter Any key to Continue -->")
                else:
                    # When exit key is press i.e -1 process config becomes None
                    process_config = process_service_functions(
                        menu_list, input_value)
                    if process_config:
                        process_config = process_accounts(process_config)
                    if process_config:
                        process_config = process_regions(process_config)
                    if process_config:
                        process_config = process_paginatio_attributes(
                            process_config)
                    if process_config:
                        process_config["attributes"] = dict(menu_util.MenuData.get_attributes(
                        ))
                        core_processor.process(process_config)
        except ValueError as e:
            if str(e) == "Please configure Master Account":
                print("Please configure Master Account")



def process_service_functions(menu_list, input_value):
    in_process_service_functions = True
    process_config = None
    while in_process_service_functions:
        menu_util.print_menu_data(menu_list, input_value)
        option_selected_value = input("Please enter option HERE-->").strip()
        if option_selected_value == "-1":
            break
        else:
            menu_item = validate_menu(option_selected_value, menu_list)
            if menu_item:
                process_config = menu_util.MenuData.get_menu_item(
                    menu_item)
                process_config = dict(process_config)
                in_process_service_functions = False
                break
            else:
                print("Invalid option selected .Please try again")
                #process_service_functions(menu_list, input_value)
    return process_config


def process_accounts(process_config):
    in_process_accounts = True

    if process_config["is_multi_account_support"] == "yes":
        while in_process_accounts:
            accounts = input(
                "Please enter comma seperated account id(s) or ALL  HERE--> ").strip()
            if accounts == "-1":
                process_config = None
                in_process_accounts = False
                break
            else:
                account_list = menu_util.MenuData.get_account_list()
                if accounts.upper() == "ALL":
                    process_config["accounts"] = account_list
                    in_process_accounts = False
                    break
                else:
                    account_list_selected = accounts.split(',')
                    validated_account_list = validated_list_value(
                        account_list_selected, account_list)
                    if len(validated_account_list) > 0:
                        process_config["accounts"] = validated_account_list
                        in_process_accounts = False
                        break
                    else:
                        print("Please enter valid accounts : Valid accounts are .. ")
                        menu_util.print_accounts()

    else:
        while in_process_accounts:
            account_selected = input(
                "Please enter account id  HERE--> ").strip()
            if account_selected == "-1":
                process_config = None
                break
            else:
                account_list = menu_util.MenuData.get_account_list()
                account_list_selected = []
                account_list_selected.append(account_selected)
                validated_account_list = validated_list_value(
                    account_list_selected, account_list)
                if len(validated_account_list) > 0:
                    process_config["accounts"] = validated_account_list
                    break
                else:
                    print("Please enter valid accounts : Valid accounts are .. ")
                    menu_util.print_accounts()

    return process_config


def process_regions(process_config):
    in_process_regions = True
    if process_config["is_regional"] == "yes":
        while in_process_regions:
            regions = input(
                "Please enter comma seperated regions(s) or ALL  HERE--> ").strip()
            if regions == "-1":
                process_config = None
                in_process_regions = False
                break
            else:
                region_list = menu_util.MenuData.get_region_list()
                if regions.upper() == "ALL":
                    process_config["regions"] = region_list
                    break
                else:
                    regions_list_selected = regions.split(',')
                    validated_regions_list = validated_list_value(
                        regions_list_selected, region_list)
                    if len(validated_regions_list) > 0:
                        process_config["regions"] = validated_regions_list
                        in_process_regions = False
                        break
                    else:
                        print("Please enter valid regions : Valid regions are .. ")
                        menu_util.print_regions()
    return process_config


def process_paginatio_attributes(process_config):
    if "pagination_attributes" in process_config.keys():
        refined_pagination_attributes = {}
        for pagination_attribute in process_config["pagination_attributes"]:
            if pagination_attribute["is_visible"].upper() == "YES":
                pagination_attribute_value = input(
                    "{} HERE--> ".format(pagination_attribute["display_prompt"])).strip()
                if pagination_attribute_value == "-1":
                    process_config = None
                    break
                else:
                    refined_pagination_attributes[pagination_attribute["attribute_name"]
                                                  ] = pagination_attribute_value
            else:
                refined_pagination_attributes[pagination_attribute["attribute_name"]
                                              ] = pagination_attribute["attribute_value"]
        process_config["pagination_attributes"] = refined_pagination_attributes

    return process_config


def validate_menu(menu_item, menu_list):
    valid_menu_item = None
    if menu_item in [x["menu_index"] for x in menu_list]:
        valid_menu_item = menu_item
    # This if user enters number as option like 1,2
    else:
        if menu_item. isdigit():
            menu_item_index = int(menu_item)-1
            if menu_item_index <= len(menu_list):
                valid_menu_item = menu_list[menu_item_index]["menu_index"]
    return valid_menu_item


def validated_list_value(input_list, to_compare_list):
    validate_list = []
    for item in input_list:
        if item.strip() in to_compare_list:
            validate_list.append(item.strip())
    return validate_list
