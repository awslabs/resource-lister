import botocore
from resource_lister.session_mgr.iam_session_mgr import IAMSessionManager
from resource_lister.session_mgr.iam_session_mgr import AccountConfig


class SessionHandler():
    __session_cache = dict()
    __master_account_session = None
    __count = 0

    @classmethod
    def __get_session_from_session_mgr(cls, account):
        SessionHandler.__count = SessionHandler.__count+1
        return IAMSessionManager.get_iam_session(account)

    @classmethod
    def get_master_account_session(cls):
        if SessionHandler.__master_account_session is None:
            master_account = AccountConfig.get_master_account()["account_id"]
            SessionHandler.__master_account_session = IAMSessionManager.get_iam_session(master_account)
        return SessionHandler.__master_account_session


    @classmethod
    def get_session(cls, account):
        if account not in SessionHandler.__session_cache:
            SessionHandler.__session_cache[account] = SessionHandler.__get_session_from_session_mgr(
                account)
        return SessionHandler.__session_cache[account]
    
    
    @classmethod
    def get_new_session(cls, account):
        return IAMSessionManager.get_iam_session(account)

