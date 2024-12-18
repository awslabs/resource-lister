"""
This is supporting functions to update config.json
"""
import json
import os
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()


class ConfigAttributes():
    """
    ConfigAttributes maintains utilities configurations like format_type, s3 bucket
    ConfigAttributes class hold the values for config.json
    """
    __data = None

    @classmethod
    def __get_file_path(cls) -> str:
        """

        :param path: Request path
        :param query: Querystring
        :return: complete path of account_config.json
        """
        __CONFIG_FILE = "config.json"
        dir_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(dir_path, __CONFIG_FILE)
        return file_path

    @classmethod
    def load_config_attributes(cls) -> dict:
        """
        :return: config attributes.json
        """

        try:
            f = open(ConfigAttributes.__get_file_path())
            ConfigAttributes.__data = json.load(f)
        except FileNotFoundError:
            logger.error(" config.json {} is not found ".format(
                ConfigAttributes.__get_file_path()))

        return ConfigAttributes.__data

    @classmethod
    def get_config_attributes(cls) -> dict:
        """
        :return: config attributes.json
        """
        if ConfigAttributes.__data is None:
            ConfigAttributes.load_config_attributes()

        return ConfigAttributes.__data

    @classmethod
    def update_config_attributes(cls, json_data) -> None:
        """
        Update the config.json file 
        :param json_data: data in Json format
        :return: complete path of account_config.json
        """
        file_path = ConfigAttributes.__get_file_path()
        json_object = json.dumps(json_data, indent=4, default=str)
        # Writing to sample.json
        with open(file_path, "w") as outfile:
            outfile.write(json_object)
        ConfigAttributes.load_config_attributes()



