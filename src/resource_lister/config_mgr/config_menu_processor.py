"""
This is supporting functions to update config.json
"""
import logging
import resource_lister.config_mgr.config_util as config_util
import resource_lister.util.menu_configs as config_menu_configs
import resource_lister.util.menu_util as menu_util
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


def print_configure_utility():
    """
    : Print the utility configuraiton to console
    """
    attributes = dict(config_util.ConfigAttributes.get_config_attributes())
    CONFIGURATION = "CURRENT CONFIGURATIONS :\n 1. Format Type (csv/json) : {} \n 2. Output To (print/file/s3/none) :{}\n 3. Generate only required Columns (yes/no): {}\n 4. Generate seperate file for each AWS Account (yes/no) : {}\n 5. S3 Bucket : {}\n 6. Date append to file extension : {}\n".format(
        attributes["format_type"], attributes["output_to"], attributes["required"], attributes["account_split"], attributes["s3_bucket"], attributes["file_append_date"])
    print(CONFIGURATION)


def modify_formate_type():
    """
    : modifys format_type in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.formate_type_config, input_json)
    format_type = input_json_value["format_type"].strip()
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["format_type"] = format_type
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print("Format Type is succesfully updated  to {}.".format(format_type))
    print_configure_utility()


def modify_output_to():
    """
    : modifys output_to in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.output_to_config, input_json)
    output_to = input_json_value["output_to"].strip()
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["output_to"] = output_to
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print("Output Type is succesfully updated  to {}.".format(output_to))
    print_configure_utility()


def modify_required():
    """
    : modify required in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.required_config, input_json)
    required = input_json_value["required"]
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["required"] = required
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print("Generate only required Columns updated  to {}.".format(required))
    print_configure_utility()


def modify_account_wise():
    """
    : modify account_wise option in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.account_split_config, input_json)
    account_split = input_json_value["account_split"].strip()
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["account_split"] = account_split
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print(" Generate seperate file for each AWS Account updated  to {}.".format(
        account_split))
    print_configure_utility()


def modify_s3_bucket():
    """
    : modify s3 bucket in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.s3_config, input_json)
    s3_bucket = input_json_value["s3_bucket"].strip()
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["s3_bucket"] = s3_bucket
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print(" The S3 bucket path has been successfully updated. {}.".format(s3_bucket))
    print_configure_utility()


def modify_file_append_date():
    """
    : modify s3 bucket in config.json
    """
    input_json = dict()
    input_json_value = menu_util.process_inputs(
        config_menu_configs.file_append_date_config, input_json)
    file_append_date = input_json_value["file_append_date"].strip()
    config_attributes = dict(
        config_util.ConfigAttributes.get_config_attributes())
    config_attributes["file_append_date"] = file_append_date
    config_util.ConfigAttributes.update_config_attributes(config_attributes)
    # Print statement to print output to command prompt
    print(" Date extension will be appended to generated file{}.".format(file_append_date))
    print_configure_utility()



