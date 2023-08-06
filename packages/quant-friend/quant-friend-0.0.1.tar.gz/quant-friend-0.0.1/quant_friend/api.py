class HostIdentifier:
    """
主机识别符，无论何种供应商，都只支持这个主机识别符
    """

    def __init__(self, identifier: str, brand: str):
        super(HostIdentifier, self).__init__()
        self.identifier = identifier
        self.brand = brand
