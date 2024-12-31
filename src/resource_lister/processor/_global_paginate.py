import botocore
from resource_lister.util.session_util import SessionHandler
from resource_lister.util.s3_util import S3Uploader
from resource_lister.boto_formatter.service_formatter import service_response_formatter
import logging
import datetime
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def process(process_config):
    object_list = []
    accounts = process_config["accounts"]
    service_name = process_config["service_name"]
    function_name = process_config["function_name"]
    attributes = process_config["attributes"]
    attributes["pagination"] = "True"
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    pagination_attributes = None
    __result = None
    if "pagination_attributes" in process_config.keys():
        pagination_attributes = process_config["pagination_attributes"]
# YES: generate seperate output file for each account
    if attributes["account_split"].lower() == "yes":
        for _account in accounts:
            _session = SessionHandler.get_session(_account)
            object_list = []
            object_list.append(process_global_list(
                _session, _account, service_name, function_name, current_date, pagination_attributes))
            __result = process_result(process_config, service_response_formatter(
                service_name, function_name, object_list, attributes))
# NO: Generate Consolidated output for all the accounts
    else:
        for _account in accounts:
            _session = SessionHandler.get_session(_account)
            object_list.append(process_global_list(
                _session, _account, service_name, function_name, current_date, pagination_attributes))
        __result = process_result(process_config, service_response_formatter(
            service_name, function_name, object_list, attributes))
    return __result


def process_global_list(_session, _account, service_name, function_name, current_date, pagination_attributes):
    """
    Functions with Paginator
    """
    result = dict()
    object_list = []
    try:
        prefix_columns = dict()
        prefix_columns["Account"] = _account
        prefix_columns["Creation_Date"] = current_date
        prefix_columns["service_name"] = service_name
        prefix_columns["function_name"] = function_name
        service_func = _session.client(service_name)
        paginator = service_func.get_paginator(function_name)
        page_iterator = None
        if pagination_attributes:
            # AccountId attribute would be changed to current account value
            for key in pagination_attributes:
                if key == "AccountId":
                    pagination_attributes[key] = _account
            page_iterator = paginator.paginate(**pagination_attributes)
        else:
            page_iterator = paginator.paginate()
        for page in page_iterator:
            object_list.append(page)
        result['prefix_columns'] = prefix_columns
        result['result'] = object_list

    except botocore.exceptions.ClientError as error:
        logger.debug("ERROR {}".format(error))
        logger.debug("Service {}".format(service_name))
        logger.debug("Function Name {}".format(function_name))
        logger.debug("Pagination_attributes {}".format(pagination_attributes))
        # Invalid attributes throws client errors
        result['prefix_columns'] = prefix_columns
        result['result'] = object_list
    except botocore.exceptions.ParamValidationError as error:
        logger.debug("ERROR {}".format(error))
        raise ValueError(
            'The parameters you provided are incorrect: {}'.format(error))
    return result


def process_result(process_config, result):
    attributes = process_config["attributes"]
    # boto_formatter understand only file or print
    if attributes["output_to"] == "s3":
        S3Uploader().upload_file(dict(process_config), result)
    return result
