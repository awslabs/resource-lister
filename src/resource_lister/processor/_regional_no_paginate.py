import concurrent.futures
import botocore
from resource_lister.boto_formatter.service_formatter import service_response_formatter
from resource_lister.util.session_util import SessionHandler
from resource_lister.util.s3_util import S3Uploader
import logging
import datetime
from botocore.config import Config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def process(process_config):
    accounts = process_config["accounts"]
    regions = process_config["regions"]
    service_name = process_config["service_name"]
    function_name = process_config["function_name"]
    attributes = process_config["attributes"]
    current_date = datetime.datetime.now().strftime("%m/%d/%Y")
    attributes["pagination"] = "False"
    # pagination attributes are attributes passed to function
    pagination_attributes = None
    __result = None
    if "pagination_attributes" in process_config.keys():
        pagination_attributes = process_config["pagination_attributes"]
    object_list = []
# YES: generate seperate output file for each account
    if attributes["account_split"].lower() == "yes":
        for account in accounts:
            object_list = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Start the load operations and mark each future with its URL
                futures = {executor.submit(process_region_list_pagination, SessionHandler.get_new_session(account), account, region,
                                           service_name, function_name, current_date, pagination_attributes): region for region in regions}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        object_list.append(future.result())
                    except Exception as exc:
                        logger.error(exc)
            process_result(process_config, service_response_formatter(
                service_name, function_name, object_list, attributes))
# NO: Generate Consolidated output for all the accounts
    else:
        for account in accounts:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                # Start the load operations and mark each future with its URL
                futures = {executor.submit(process_region_list_pagination, SessionHandler.get_new_session(account), account, region,
                                           service_name, function_name, current_date, pagination_attributes): region for region in regions}
                for future in concurrent.futures.as_completed(futures):
                    try:
                        object_list.append(future.result())
                    except Exception as exc:
                        logger.error(exc)
        __result = process_result(process_config, service_response_formatter(
            service_name, function_name, object_list, attributes))
    return __result


def process_region_list_pagination(_session, account, _region, service_name, function_name, current_date, pagination_attributes):
    """Regional functions with no pagination"""
    result = dict()
    object_list = []
    prefix_columns = dict()
    prefix_columns["Account"] = account
    prefix_columns["Region"] = _region
    prefix_columns["Creation_Date"] = current_date
    try:
        _session_client = _session.client(
            service_name, config=Config(region_name=_region))
        if pagination_attributes:
            object_list = getattr(_session_client, function_name)(
                **pagination_attributes)
        else:
            object_list = getattr(_session_client, function_name)()
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
