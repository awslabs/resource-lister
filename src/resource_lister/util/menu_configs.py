

formate_type_config = [{
    "id": "format_type",
    "display_prompt": "Format Type (csv/json)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "validate_format"]
}
]

output_to_config = [{
    "id": "output_to",
    "display_prompt": "Output To (print/file/s3/none)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "validate_output_to"]
}
]

required_config = [{
    "id": "required",
    "display_prompt": "Generate only required Columns(yes/no)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
}
]

account_split_config = [{
    "id": "account_split",
    "display_prompt": "Generate seperate file for each AWS Account(yes/no)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
}
]
s3_config = [{
    "id": "s3_bucket",
    "display_prompt": "S3 Bucket Name",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
}]


file_append_date_config = [{
    "id": "file_append_date",
    "display_prompt": "Do you want to append date to generated file (yes/no)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
}]


config_menu_config = {
    "menu": {
        "0": {
            "menu_link": "MENU [MAIN-->HELP-->Manage Configurations]:",
            "menu_question": "Please select any of following option:",
            "menu_options": [
                {"display_name": "Current Configurations.",
                 "action": "True",
                 "function_name": "print_configure_utility"

                 },
                {"display_name": "Modify Format Type (csv/json).",
                 "action": "True",
                 "function_name": "modify_formate_type"

                 },
                {"display_name": "Modify  Output To (print/file/s3).",
                 "action": "True",
                 "function_name": "modify_output_to"

                 },
                {"display_name": "Modify  Generate only required Columns",
                 "action": "True",
                 "function_name": "modify_required"

                 },
                {"display_name": "Modify  Seperate file for each AWS Account",
                 "action": "True",
                 "function_name": "modify_account_wise"
                 },
                {"display_name": "Modify S3 Bucket Name",
                 "action": "True",
                 "function_name": "modify_s3_bucket"
                 },
                {"display_name": "Modify File append date option",
                 "action": "True",
                 "function_name": "modify_file_append_date"
                 },

            ]
        }

    }
}

master_account_config = [
    {
        "id": "account_id",
        "display_prompt": "Account ID (12-digit account ID)",
        "is_mandatory": "yes",
        "validation_functions": ["validate_mandatory", "check_12_digit"]
    },
    {
        "id": "account_description",
        "display_prompt": "Account Description",
        "is_mandatory": "yes",
        "validation_functions": ["validate_mandatory"]
    },

    {
        "id": "account_config_type",
        "display_prompt": "Master account role access configuration \n [1. Use default credentials] \n [2. Assume master account role from default credentials ] \n ENTER HERE-->",
        "is_mandatory": "yes",
        "validation_functions": ["validate_mandatory", "check_account_config_type"]
    },

    {
        "id": "master_account_role_arn",
        "display_prompt": "Master account IAM role ARN:",
        "is_mandatory": "yes",
        "validation_functions": ["validate_mandatory", "validate_arn"],
    },


    {
        "id": "child_account_assume_role_name",
        "display_prompt": "Child account role name",
        "is_mandatory": "yes",
        "validation_functions": ["validate_mandatory"]
    },
    {
        "id": "email",
        "display_prompt": "Email:",
        "is_mandatory": "no",
        "validation_functions": ["validate_mandatory"]
    }



]

child_account_modify_config = [
    {
    "id": "account_id",
    "display_prompt": "Account ID (12 digit account ID)",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "check_12_digit"]
},
    {
    "id": "account_description",
    "display_prompt": "Account Description",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
},
    
    {
    "id": "policy",
    "display_prompt": "Policy ReadOnlyAccess",
    "is_mandatory": "no",
}]

child_account_config = [{
    "id": "account_ids",
    "display_prompt": "Enter comma separated child account ids",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "validate_accounts"]
}

]

master_account_arn_config = [{
    "id": "master_account_role_arn",
    "display_prompt": "Master account IAM role/IAM user Arn",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "validate_arn"]
},
    {
    "id": "account_config_type",
    "display_prompt": "Master account role access configuration \n [1. Use default credentials] \n [2. Assume master account role from default credentials ] \n ENTER HERE-->",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "check_account_config_type"]
},
    {
    "id": "child_account_assume_role_name",
    "display_prompt": "Child account role name ",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory"]
}

]

child_account_delete_config = [{
    "id": "account_ids",
    "display_prompt": "Enter comma separated child account ids to be deleted",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory", "validate_accounts"]
}]


account_menu_config = {
    "menu": {
        "0": {
            "menu_link": "MENU [MAIN-->HELP-->Manage AWS Account]",
            "menu_question": "Please select any of following option:",
            "menu_options": [
                {"display_name": "Add Master Account.",
                 "action": "True",
                 "function_name": "configure_master_arn_config"

                 },
                {"display_name": "Modify Master Account",
                 "action": "True",
                 "function_name": "process_master_account"

                 },
                {"display_name": "Generate cloudformation template for Child Account",
                 "action": "True",
                 "function_name": "process_cfn_template"

                 },
                {"display_name": "Configure Child Accounts",
                 "action": "True",
                 "function_name": "process_upsert_child_account"
                 },
                {"display_name": "Modify Child Account",
                 "action": "True",
                 "function_name": "modify_child_account"
                 },
                {"display_name": "List all Child Accounts",
                 "action": "True",
                 "function_name": "process_list_child_accounts"

                 },

                {"display_name": "Delete Child Accounts",
                 "action": "True",
                 "function_name": "process_delete_child_account"

                 }
            ]
        }

    }
}



config_generator_util_config = [{
    "id": "input_dir_path",
    "display_prompt": "Please specify the complete input directory path where the configuration files are located[example C:\\abc\\configs].",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory","check_dir_path"]
},
    {
    "id": "output_dir_path",
    "display_prompt": "Please specify the complete output directory where the  configuration files will be generated.",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory","check_dir_path"]
}

]


config_generator_upload_service_config = [{
    "id": "input_file_path",
    "display_prompt": "Please specify the complete service config file [example C:\\abc\\configs\\service_name.json].",
    "is_mandatory": "yes",
    "validation_functions": ["validate_mandatory","check_dir_path"]
}

]

config_generator_menu_config = {
    "menu": {
        "0": {
            "menu_link": "MENU [MAIN-->HELP-->Generate service configuration files]",
            "menu_question": "Please select any of following option:",
            "menu_options": [
                {"display_name": "Generate service configuration files.",
                 "action": "True",
                 "function_name": "process_config_files"

                 },
                 {"display_name": "Upload service configuration file.",
                 "action": "True",
                 "function_name": "upload_config_file"

                 }
            ]
    }
}
}


