'''
This sample, non-production-ready template Utility to estimate cross account KMS API Calls.
(c) 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.

'''
import boto3
import os
import json
import logging
from botocore.exceptions import ClientError
from typing import List, Dict, Any, Optional, Sequence, Union, Callable, Set, \
    Iterator, TYPE_CHECKING, Tuple

# Set up our logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class IAMSessionManager():
    """ Session Manager class create sessions based on configured accounts
        in account_config.json. You can use command line utility to configure accounts
        Boto sessions are not thread safe, so session manager creates session for each request
    """
    __count = 0

    @classmethod
    def __get_session_count(cls):
        IAMSessionManager.__count = + 1
        return IAMSessionManager.__count

    @classmethod
    def get_iam_session(cls, account_id) -> boto3.session.Session:
        # Get Configuration Information
        __session = None
        try:
            account = AccountConfig.get_account(account_id)
            _master_account = AccountConfig.get_master_account()
            # if master account is also present in account
            if account["IsMasterAcccount"]:
                if _master_account["account_config_type"] == "1":
                    __session = boto3.session.Session()
                else:
                    __master_account_session = boto3.session.Session()
                    _master_sts_client = __master_account_session.client('sts')
                    session_name = "IAMSessionManager_{}".format(
                        IAMSessionManager.__get_session_count())
                    master_assumed_role_object = _master_sts_client.assume_role(
                        RoleArn=_master_account["master_account_role_arn"], RoleSessionName=session_name)
                    role_credentials = master_assumed_role_object['Credentials']
                    __session = boto3.Session(
                        aws_access_key_id=role_credentials['AccessKeyId'], aws_secret_access_key=role_credentials['SecretAccessKey'], aws_session_token=role_credentials['SessionToken'])
            # Master account session is required only when it's IAM Role
            else:
                # If master account is based on default credentials
                sts_client = None
                if _master_account["account_config_type"] == "1":
                    # if account is role get session from instance profile
                    __master_account_session = boto3.session.Session()
                    sts_client = __master_account_session.client('sts')
                else:
                    # if it's IAM user first get session from Master Account IAM Role
                    # Then get sts session for child account
                    __master_account_session = boto3.session.Session()
                    _master_sts_client = __master_account_session.client('sts')
                    session_name = "IAMSessionManager_{}".format(
                        IAMSessionManager.__get_session_count())
                    master_assumed_role_object = _master_sts_client.assume_role(
                        RoleArn=_master_account["master_account_role_arn"], RoleSessionName=session_name)
                    role_credentials = master_assumed_role_object['Credentials']
                    role__session = boto3.Session(
                        aws_access_key_id=role_credentials['AccessKeyId'], aws_secret_access_key=role_credentials['SecretAccessKey'], aws_session_token=role_credentials['SessionToken'])
                    sts_client = role__session.client('sts')

                session_name = "IAMSessionManager_{}".format(
                    IAMSessionManager.__get_session_count())
                assumed_role_object = sts_client.assume_role(
                    RoleArn=account["role_arn"], RoleSessionName=session_name)
                # From the response that contains the assumed role, get the temporary
                # credentials that can be used to make subsequent API calls
                credentials = assumed_role_object['Credentials']
                __session = boto3.Session(
                    aws_access_key_id=credentials['AccessKeyId'],
                    aws_secret_access_key=credentials['SecretAccessKey'], aws_session_token=credentials['SessionToken'])

            logger.info("Created new session for account --> {}".format(
                account["account_id"]))
        except ClientError as err:
            logging.error(err)
            logger.exception(
                "Couldn't create session for account %s.", account_id)
            raise

        return __session


class AccountConfig():
    """ This class hold the  values from account_config.json"""

    __master_account = None
    __accounts = dict()
    __data = None
    __CONFIG_FILE = "account_config.json"

    def __init__(self):
        AccountConfig.load_data()

    @classmethod
    def load_data(cls):
        # Opening JSON file
        try:
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, AccountConfig.__CONFIG_FILE)
            f = open(file_path)
            __data = json.load(f)
            AccountConfig.__master_account = __data["master_account"]
            if AccountConfig.__master_account["account_id"].strip() == "":
                raise ValueError("Please configure Master Account")
            else:
                AccountConfig.__master_account["IsMasterAcccount"] = True
                # Add first account as master account
                AccountConfig.__accounts[AccountConfig.__master_account["account_id"]
                                         ] = AccountConfig.__master_account
                # Flat the account json
                # check if default role or custom role
                # default role is created via CFN provided by utility
                child_account_assume_role_name = AccountConfig.__master_account[
                    "child_account_assume_role_name"]

                if "accounts" in __data.keys():
                    for account in __data["accounts"]:
                        account_dict = dict()
                        account_dict["account_id"] = account["account_id"]
                        account_dict["account_description"] = account["account_description"]
                        account_dict["role_arn"] = "arn:aws:iam::{}:role/{}".format(
                            account["account_id"], child_account_assume_role_name)
                        account_dict["IsMasterAcccount"] = False
                        AccountConfig.__accounts[account["account_id"]
                                                 ] = account_dict
                f.close()
        except KeyError as err:
            logger.error(
                "Please check aws_account_config.json file . File syntax is not correct.")
            raise err
        except FileNotFoundError as err:
            logger.error(
                "File aws_account_config.json is not Found. Please check aws_account_config.json file exists")
            raise err
        except IOError as err:
            logger.error(
                " IO error while loading the file aws_account_config.json {}. ".format(err))
            raise err

    @ classmethod
    def get_master_account(cls) -> Dict[str, Any]:
        if AccountConfig.__data is None:
            AccountConfig.load_data()
        return AccountConfig.__master_account

    @ classmethod
    def get_account_list(cls) -> List[str]:
        if AccountConfig.__data is None:
            AccountConfig.load_data()
        return list(AccountConfig.__accounts.keys())

    @ classmethod
    def get_accounts(cls) -> Dict[str, Any]:
        if AccountConfig.__data is None:
            AccountConfig.load_data()
        return AccountConfig.__accounts

    @ classmethod
    def get_account(cls, account_alias) -> Dict[str, Any]:
        if AccountConfig.__data is None:
            AccountConfig.load_data()
        return AccountConfig.__accounts[account_alias]

    @ classmethod
    def print_account_list(cls, all_account_true=True):
        if AccountConfig.__data is None:
            AccountConfig.load_data()
        print("REFERENCE--> ** Account configured in utility **")
        print("{}|{}".format( "Acccount ID", "Account Description","Master Account"))
        if all_account_true:
            print("{}|{}|{}".format("ALL", "ALL", "False"))
        for account_id in AccountConfig.get_account_list():
            account = AccountConfig.get_account(account_id)
            print("{}|{}|{}".format(
                 account["account_id"],account["account_description"], account["IsMasterAcccount"]))

    @ classmethod
    def is_valid_account(cls, account_id, all_account_true=True):
        is_valid = False
        if all_account_true:
            if account_id == "ALL":
                is_valid = True
        if not is_valid:
            for account in AccountConfig.get_account_list():
                if account == account_id:
                    is_valid = True
                    break
        return is_valid


class Region():
    """ This class hold the  regions"""
    __regions = None

    @classmethod
    def __load_regions(cls):
        __session = IAMSessionManager().get_iam_session(
            AccountConfig.get_master_account()["account_id"])
        ec2_client = __session.client('ec2')
        Region.__regions = [region['RegionName']
                            for region in ec2_client.describe_regions()['Regions']]

    @classmethod
    def get_regions(cls):
        if Region.__regions:
            return Region.__regions
        else:
            Region.__load_regions()
            return Region.__regions

    @classmethod
    def is_valid_region(cls, region_name, all_region_support=True):
        if all_region_support:
            if region_name == "ALL":
                return True
        if Region.__regions:
            return region_name in Region.__regions
        else:
            Region.__load_regions()
            return region_name in Region.__regions

    @classmethod
    def print_regions(cls, all_region_support=True):
        if all_region_support:
            print("ALL")
        if Region.__regions:
            for region in Region.__regions:
                print(region)
