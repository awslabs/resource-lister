import logging
import resource_lister.session_mgr.account_config_util as account_config_util
import resource_lister.util.menu_configs as acounts_menu_configs
import resource_lister.util.menu_util as menu_util
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def configure_master_arn_config():
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        acounts_menu_configs.master_account_arn_config, input_json)
    master_account_role_arn = input_json_value["master_account_role_arn"].strip()
    input_json["account_id"] = master_account_role_arn[13:25]
    input_json["account_description"] = "Master Account "
    input_json["account_config_type"] = input_json_value["account_config_type"].strip()
    input_json["master_account_role_arn"] = master_account_role_arn
    input_json["child_account_assume_role_name"] = input_json_value["child_account_assume_role_name"].strip()
    input_json["email"] = ""
    account_config_util.upsert_master_account(input_json)
    # Print statement to print output to command prompt
    print("Master Account configured succesfully.")
    process_cfn_template()


def process_master_account():
    input_json = dict()
    master_account_data = account_config_util.print_master_account_details()
    if master_account_data:
        print(
            "Update Master account here with new details ************************************************")
    else:
        print(
            "Add New Master account here  ************************************************")
    input_json = menu_util.process_inputs(
        acounts_menu_configs.master_account_config, input_json)
    account_config_util.upsert_master_account(input_json)
    # Print statement to print output to command prompt
    print("Master Account updated succesfully")
    process_cfn_template()


def process_cfn_template():
    master_account_config = account_config_util.get_account_config_data()[
        "master_account"]
    file_path = account_config_util.generate_cfn_template(
        master_account_config["master_account_role_arn"],
        master_account_config["child_account_assume_role_name"])
    print("Cloudformation template generatd at location {} ".format(file_path))


def process_list_child_accounts():
    account_config_util.print_child_account_details()


def process_upsert_child_account():
    input_json = dict()
    account_json_list = []
    input_json = menu_util.process_inputs(
        acounts_menu_configs.child_account_config, input_json)
    account_ids_list = input_json["account_ids"].split(",")
    master_account_config = account_config_util.get_account_config_data()["master_account"]
    master_account_id = master_account_config["account_id"].strip()
    print(master_account_id)
    for account_id in account_ids_list:
        account_id = account_id.strip()
        if account_id != master_account_id:
            account_json = {}
            account_json["account_id"] = account_id
            account_json["account_description"] = "To access Account {}".format(
                account_id)
            account_json["policy"] = "ReadOnlyAccess"
            account_json_list.append(account_json)
        else:
            print("Skipping child account which has same account_id as master account {} ".format(master_account_id))

    account_config_util.upsert_child_account(account_json_list)
    input("Press Ok when you have succesfully the cloudformation template in accounts : \n ")


def modify_child_account():
    input_json = dict()
    input_json = menu_util.process_inputs(
        acounts_menu_configs.child_account_modify_config, input_json)
    master_account_config = account_config_util.get_account_config_data()["master_account"]
    master_account_id = master_account_config["account_id"].strip()
    if input_json["account_id"] == master_account_id:
        print("Child account can't have same account_id as master account {}".format(master_account_id))
    else:
        account_config_util.modify_child_account(input_json)
    print("Child Account  modified  succesfully")


def process_delete_child_account():
    input_json = dict()
    account_json_list = []
    input_json = menu_util.process_inputs(
        acounts_menu_configs.child_account_delete_config, input_json)
    account_ids_list = input_json["account_ids"].split(",")
    for account_id in account_ids_list:
        account_id = account_id.strip()
        account_json_list.append(account_id)
    account_config_util.delete_child_account(account_json_list)
    print("Child Account  deleted  succesfully")
    print(
        "Please also delete the stack created by cloudformation template [cfn_child_account_template] in child account")
