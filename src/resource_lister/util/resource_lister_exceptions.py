class ResourceListerExcpetion(Exception):
    pass


class MasterAccountExcpetion(ResourceListerExcpetion):
    STATUS_CODE: int = 100
    

class MasterAccountExcpetion(ResourceListerExcpetion):
    STATUS_CODE: int = 100