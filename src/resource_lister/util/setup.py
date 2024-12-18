import resource_lister.util.menu_configs as menu_configs
import resource_lister.util.config_generator_util as config_generator_util
import resource_lister.config_mgr.config_menu_processor as config_menu_processor
import resource_lister.session_mgr.accounts_menu_processor as accounts_menu_processor
import resource_lister.util.menu_util as menu_util


def process_config_setup():
    """Config Setup menu"""
    menu = menu_util.Menu(menu_configs.config_menu_config)
    menu_util.MenuProcessor(menu, config_menu_processor).process_menu()


def process_account_setup():
    """Account Setup menu"""
    menu = menu_util.Menu(menu_configs.account_menu_config)
    menu_util.MenuProcessor(menu, accounts_menu_processor).process_menu()


def generate_configfiles_setup():
    """Generate Config Files"""
    menu = menu_util.Menu(menu_configs.config_generator_menu_config)
    menu_util.MenuProcessor(menu, config_generator_util).process_menu()