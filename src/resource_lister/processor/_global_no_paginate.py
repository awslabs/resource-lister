"""
Library to process functions which are global and doesn't have pagination support
example : s3 list_buckets
"""
import botocore
from resource_lister.util.session_util import SessionHandler
from resource_lister.util.s3_util import S3Uploader
from resource_lister.boto_formatter.service_formatter import service_response_formatter
import logging
import datetime
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def process(process_config):
    object_list = []
    accounts = process_config["accounts"]
    service_name = process_config["service_name"]
    function_name = process_config["function_name"]
    attributes = process_config["attributes"]
    attributes["pagination"] = "False"
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    # pagination attributes are attributes passed to function
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
                _session, _account, service_name, function_name, current_date, pagination_attributes,))
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
    Process global service no paginates
    """
    result = dict()
    object_list = []
    try:
        prefix_columns = dict()
        prefix_columns["Account"] = _account
        prefix_columns["Creation_Date"] = current_date
        prefix_columns["service_name"] = service_name
        prefix_columns["function_name"] = function_name
        _session_client = _session.client(service_name)
        if pagination_attributes:
            object_list = getattr(_session_client, function_name)(
                **pagination_attributes)
        else:
            object_list = getattr(_session_client, function_name)()
        result['prefix_columns'] = prefix_columns
        result['result'] = object_list
    except botocore.exceptions.ClientError as error:
        logger.error("In valid attributes {}".format(pagination_attributes))
        # Invalid attributes throws client errors
        result['prefix_columns'] = prefix_columns
        result['result'] = object_list
    except botocore.exceptions.ParamValidationError as error:
        logger.error(error)
        raise ValueError(
            'The parameters you provided are incorrect: {}'.format(error))
    return result


def process_result(process_config, result):
    attributes = process_config["attributes"]
    # boto_formatter understand only file or print
    if attributes["output_to"] == "s3":
        S3Uploader().upload_file(dict(process_config), result)
    return result
