from datetime import datetime
import os
from resource_lister.util.session_util import SessionHandler
from botocore.exceptions import ClientError
import resource_lister.menu.menu_util as menu_util
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


class S3Uploader():
    def upload_file(self, process_config, file_full_path):
        # Get full file path
        partition = "misc"
        attributes = process_config["attributes"]
        if file_full_path:
            datetime_object = datetime.now().strftime("%Y-%m-%d")
            path_list = file_full_path.split(os.path.sep)
            file_name = path_list[(len(path_list)-1)]
            partition = "misc"
            s3key = "data/{}/date={}/{}".format(partition,
                                                datetime_object, file_name)
            if "is_batch" in attributes.keys():
                account = process_config["accounts"][0]
                service_name = process_config["service_name"]
                function_name = process_config["function_name"]
                file_extention = file_name.split(".")[1]
                file_name = "{}_{}_{}.{}".format(
                    service_name, function_name, datetime_object, file_extention)
                s3key = "data/batch/{}/date={}/{}_{}.{}".format(
                    account, datetime_object, service_name, function_name, file_extention)

            _session = SessionHandler.get_master_account_session()
            s3_bucket = menu_util.MenuData.get_attributes()["s3_bucket"]
            try:
                s3_client = _session.client('s3')
                s3_client.upload_file(file_full_path, s3_bucket, s3key)
                print("S3: File is loaded--> {}/{}".format(s3_bucket, s3key))
                self.clean_up(file_full_path)
            except ClientError as e:
                if str(e)!="An error occurred (InvalidAccessKeyId) when calling the ListBuckets operation: The AWS Access Key Id you provided does not exist in our records.":
                    logging.error(e)



    def clean_up(self, file_full_path):
        print("Removing file {}".format(file_full_path))
        if os.path.exists(file_full_path):
            os.remove(file_full_path)
