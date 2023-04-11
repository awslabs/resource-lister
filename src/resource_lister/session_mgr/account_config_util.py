import json
import os
import logging


# Set up our logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()

cfn_template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "This template will create IAM role in child account ",
    "Resources": {
        "MyIAMRole": {
            "Type": "AWS::IAM::Role",
            "Properties": {
                "Description": "Myrole created by CFN",
                "AssumeRolePolicyDocument": {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "AWS": "TBD"
                            },
                            "Action": "sts:AssumeRole"
                        }
                    ]
                },
                "ManagedPolicyArns": [
                    "arn:aws:iam::aws:policy/ReadOnlyAccess"
                ],
                "Path": "/",
                "RoleName": "TBD"
            }
        }
    },
    "Outputs": {
        "MyIAMRoleValue": {
            "Value": {
                "Fn::GetAtt": [
                    "MyIAMRole",
                    "Arn"
                ]
            }
        }
    }
}


def get_file_path() -> str:
    """

    :param path: Request path
    :param query: Querystring
    :return: complete path of account_config.json
    """
    __CONFIG_FILE = "account_config.json"
    dir_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_path, __CONFIG_FILE)
    return file_path


def get_account_config_data() -> dict:
    """
    :return: dictionary of account_config.json
    """
    __data = dict()
    try:
        f = open(get_file_path())
        __data = json.load(f)
    except FileNotFoundError:
        logger.error("Account config {} is not found ".format(get_file_path()))

    return __data


def update_account_config(json_data) -> None:
    """
    Update the account_config.json file 
    :param json_data: data in Json format
    :return: complete path of account_config.json
    """
    file_path = get_file_path()
    json_object = json.dumps(json_data, indent=4, default=str)
    # Writing to sample.json
    with open(file_path, "w") as outfile:
        outfile.write(json_object)


def upsert_master_account(master_account_json) -> None:
    """
    Update the master_account in account_config.json file 
    :param master_account_json: data in Json format
    :return: None
    """
    accoun_config_data = get_account_config_data()
    accoun_config_data["master_account"] = master_account_json
    # Write the JSON File
    update_account_config(accoun_config_data)
    logger.debug("Master account {} succesfully added".format(
        master_account_json["account_id"]))


def upsert_child_account(account_json_list) -> None:
    """
     Update the child account in account_config.json file 
    :param child account: data in Json format
    :return: None
    """
    accoun_config_data = get_account_config_data()
    child_accounts = []
    account_json_list
    if "accounts" in accoun_config_data.keys():
        # update already exists accounts
        for account in accoun_config_data["accounts"]:
            account_present = False
            for account_json in account_json_list:

                if account_json["account_id"] == account["account_id"]:
                    child_accounts.append(account_json)
                    account_present = True
                    break
            if not account_present:
                child_accounts.append(account)
        # Add remaining accounts.
        for account_json in account_json_list:
            account_present = False
            for child_account in child_accounts:
                if account_json["account_id"] == child_account["account_id"]:
                    account_present = True
                    break
            if not account_present:
                child_accounts.append(account_json)
        accoun_config_data["accounts"] = child_accounts

    else:
        for account_json in account_json_list:
            child_accounts.append(account_json)
            accoun_config_data["accounts"] = child_accounts
    # Write the JSON file
    update_account_config(accoun_config_data)
    logger.debug("Child accounts are succesfully added")


def modify_child_account(account_json) -> None:
    """
     Modify the child account in account_config.json file 
    :param child account: data in Json format
    :return: None
    """
    accoun_config_data = get_account_config_data()
    child_accounts = []
    if "accounts" in accoun_config_data.keys():
        # update already exists accounts
        for account in accoun_config_data["accounts"]:
            if account_json["account_id"] == account["account_id"]:
                child_accounts.append(account_json)
            else:
                child_accounts.append(account)

        accoun_config_data["accounts"] = child_accounts
    update_account_config(accoun_config_data)
    logger.debug("Child account succesfully modified")


def delete_child_account(account_list) -> None:
    """
     Delete the child account from account_config.json file 
    :param child_account_name: str
    :return: None
    """
    logger.debug(account_list)
    accoun_config_data = get_account_config_data()
    child_accounts = []
    if "accounts" in accoun_config_data.keys():
        # update already exists accounts
        for account in accoun_config_data["accounts"]:
            account_present = False
            for account_name in account_list:
                if account_name == account["account_id"]:
                    account_present = True
                    break
            if not account_present:
                child_accounts.append(account)
        accoun_config_data["accounts"] = child_accounts

    # Write the JSON file
    update_account_config(accoun_config_data)
    logger.debug("Child account {} succesfully deleted")


def print_master_account_details():
    master_account_data = None
    if "master_account" in get_account_config_data().keys():
        print(" Current Master Account configuration details ******************************************")
        master_account_data = get_account_config_data()["master_account"]
        for key, value in master_account_data.items():
            print("{}:{}".format(key, value))
    return master_account_data


def print_child_account_details():
    if "accounts" in get_account_config_data().keys():
        child_account_list = get_account_config_data()["accounts"]
        count = 1
        print("Child Accounts Details *********************************")
        for child_account in child_account_list:
            print("Child Account {} *********************************".format(count))
            count += 1
            for key, value in child_account.items():
                print("{}:{}".format(key, value))
    else:
        print("No child account configured ")


def get_child_accounts():
    child_accounts_list = []
    if "accounts" in get_account_config_data().keys():
        child_account_json_list = get_account_config_data()["accounts"]
        for account in child_account_json_list:
            child_accounts_list.append(account["account_id"])
    return child_accounts_list


def generate_cfn_template(master_account_entity_arn, child_account_assume_role_name, policy_type="ReadOnlyAccess"):
    if "master_account" in get_account_config_data().keys():
        func_dir_path = None
        try:
            func_dir_path = os.getcwd()
        except AttributeError as err:
            logger.error(err)
            logger.debug("running from command prompt")
        logger.debug("Function directory Path : {}".format(func_dir_path))
        file_path = os.path.join(
            func_dir_path, "cfn_child_account_template.json")
        cfn_template["Resources"]["MyIAMRole"]["Properties"]["RoleName"] = child_account_assume_role_name
        cfn_template["Resources"]["MyIAMRole"]["Properties"]["AssumeRolePolicyDocument"]["Statement"][0]["Principal"]["AWS"] = master_account_entity_arn
        json_object = json.dumps(cfn_template, indent=4, default=str)
        # Writing to sample.json
        with open(file_path, "w") as outfile:
            outfile.write(json_object)
        return file_path
    else:
        logger.error(
            " Cloudformation template can't be generated , Please setup master account first")
        raise ValueError(
            " Cloudformation template can't be generated , Please setup master account first")
