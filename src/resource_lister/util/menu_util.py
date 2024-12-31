
import logging
import os
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


OUTPUT_DIVIDER = '''
*******************************************************************************
'''


def print_line():
    print("*******************************************************************************")


class Menu():
    """ This class hold the menu values"""
    # init method or constructor

    def __init__(self, menu_data):
        self.__menu_data = menu_data

    def get_menu_item(self, menu_index):
        if self.__menu_data:
            if menu_index in self.__menu_data["menu"].keys():
                return self.__menu_data["menu"][menu_index]
            else:
                raise ValueError(
                    "menu_config.json doesn have menu {} defined".format(menu_index))
    # Just Utility method.

    def menu_next(self, menu_key, menu_option):
        menu_next = "{}_{}".format(menu_key, menu_option)
        if self.is_valid_menu_key(menu_next):
            return menu_next
        else:
            raise ValueError("In valid Menu")

    # Just Utility method.
    def menu_previous(self, menu_key):
        menu_previous = menu_key[0:menu_key.rfind("_")]
        if self.is_valid_menu_key(menu_previous):
            return menu_previous
        else:
            raise ValueError("In Valid Menu Option")

    def get_print_menu(self, menu_item):
        count = 1
        menu_option_to_print = ""
        for menu_option in menu_item["menu_options"]:
            menu_option_to_print = menu_option_to_print + \
                "{}.[{}]\n".format(count, menu_option["display_name"])
            count = count+1
        menu_to_print = "{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\nEnter Option # HERE:-->".format(
            self.__get_seperator(),
            self.__get_seperator(),
            menu_item["menu_link"],
            self.__get_seperator(),
            menu_item["menu_question"],
            menu_option_to_print,
            self.__get_exit_option(),
            self.__get_exit_seperator()
            # enter_to_print
        )
        return menu_to_print, len(menu_item["menu_options"])

    def is_valid_menu_key(self, menu_key):
        return menu_key in self.__menu_data["menu"].keys()

    def __get_seperator(self):
        return "==============================================================================="
    
    def __get_exit_seperator(self):
        return "-------------------------------------------------------------------------------"

    def __get_exit_option(self):
        return "0.[Exit]\n-1.[Return to previous menu]"


def process_complete():
    print_line()
    input("Press any key to continue the process ->: ")


def process_start():
    print_line()


class MenuProcessor():
    def __init__(self, menu, processor_module):
        self.__menu = menu
        self.__processor_module = processor_module

    def process_menu(self):
        menu_key = "0"
        menu_option = -999
        while menu_option != 0:
            try:
                menu_item = self.__menu.get_menu_item(menu_key)
                menu_to_print, menu_length = self.__menu.get_print_menu(
                    menu_item)
            except ValueError:
                print("Please select any menu option between 1 and {}".format(
                    menu_length))
            try:
                menu_option = int(input(menu_to_print))
                if menu_option == 0:
                    pass
                elif menu_option == -1:
                    menu_key = self.__menu.menu_previous(menu_key)
                else:
                    if "action" in menu_item["menu_options"][(menu_option-1)].keys():
                        # print(menu_item["function_name"])
                        print(
                            "Menu Selected --> {}".format(menu_item["menu_options"][(menu_option-1)]["display_name"]))
                        process_start()
                        getattr(self.__processor_module, menu_item["menu_options"][(
                            menu_option-1)]["function_name"])()
                        process_complete()

                    else:
                        menu_key = self.__menu.menu_next(menu_key, menu_option)
            except ValueError:
                print("Please select any menu option between 1 and {}".format(
                    menu_length))


def process_inputs(input_config_list, input_json):
    for input_config in input_config_list:
        process_input(input_config, input_json)
    return input_json


def process_input(input_config, input_json,):
    if input_config["is_mandatory"] == "yes":
        __validation_error = True
        input_value = ""
        while __validation_error:
            __validation_error = False
            message = "Enter [{}]:".format(input_config["display_prompt"])
            input_value = input(message)
            if input_value == "-1":
                raise ValueError("breaking the loop")

            for validation_function in input_config["validation_functions"]:
                __validation_error, __message = globals()[validation_function](
                    input_value, input_config["display_prompt"])
                # if validation error comes break the loop
                if __validation_error:
                    print(__message)
                    break

        input_json[input_config["id"]] = input_value
    else:
        message = "Enter [{}]:".format(input_config["display_prompt"])
        input_value = input(message)
        input_json[input_config["id"]] = input_value


def validate_mandatory(input_value, display_prompt):
    __message = None
    _validation_error = False
    if input_value == "":
        __message = "ERROR-->  {} is Mandatory ".format(display_prompt)
        _validation_error = True
    return _validation_error, __message


def validate_format(input_value, display_prompt):
    __message = None
    _validation_error = False
    input_value = input_value.strip().lower()
    print(input_value)
    if input_value != "csv" and input_value != "json":
        __message = "ERROR-->  {} .Supported format are csv and json Only ".format(
            display_prompt)
        _validation_error = True
    return _validation_error, __message


def validate_output_to(input_value, display_prompt):
    __message = None
    _validation_error = False
    input_value = input_value.strip().lower()
    if input_value != "print" and input_value != "file" and input_value != "s3" and input_value != "none":
        __message = "ERROR-->  {} Supported outputs are print /file /s3/none Only".format(
            display_prompt)
        _validation_error = True
    return _validation_error, __message


def check_12_digit(input_value, display_prompt):
    __message = None
    _validation_error = False
    if len(input_value.strip()) != 12:
        __message = "ERROR-->  {} should be 12 digit number ".format(
            display_prompt)
        _validation_error = True
    return _validation_error, __message


def validate_accounts(input_value, display_prompt):
    __message = None
    _validation_error = False
    for values in input_value.split(","):
        if len(values.strip()) != 12:
            __message = "ERROR-->  {} should be 12 digit number ".format(
                display_prompt)
            _validation_error = True
    return _validation_error, __message


def validate_arn(arn, display_prompt):
    __message = None
    _validation_error = False
    arn = arn.strip()
    error_message = "Arn is not valid {} :Please enter valid arn in format example :arn:aws:iam::12345789012:role/abc".format(
        arn)
    if arn is None:
        _validation_error = True
        __message = error_message
    elif len(arn) < 31 or arn[0:13] != "arn:aws:iam::":
        _validation_error = True
        __message = error_message
    return _validation_error, __message


def validate_child_account_policy_type(assume_policy_type, display_prompt):
    __message = None
    _validation_error = False
    error_message = "Accepted values for {}  is default or custom".format(
        display_prompt)
    if assume_policy_type is None:
        _validation_error = True
        __message = error_message
    elif assume_policy_type.lower() != "default" and assume_policy_type.lower() != "custom":
        _validation_error = True
        __message = error_message
    return _validation_error, __message


def check_account_config_type(check_account_type, display_prompt):
    __message = None
    _validation_error = False
    error_message = "Accepted values for  is 1 or 2 : 1. For  Use default credentials  2. Assume master account role from default credentials ]"
    check_account_type = check_account_type.strip()
    if check_account_type is None:
        _validation_error = True
        __message = error_message
    elif check_account_type != "1" and check_account_type != "2":
        _validation_error = True
        __message = error_message
    return _validation_error, __message


def check_dir_path(dir_path, display_prompt):
    __message = None
    _validation_error = False
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        _validation_error = True
        __message = "Directory or file path {} does not exist.".format(dir_path)
    return _validation_error, __message
