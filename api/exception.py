class ClientError(Exception):
    def __init__(self, response, code=400):
        super(ClientError, self).__init__()
        self.response = response
        self.code = code

    def __str__(self):
        return f'ClientError: {self.response}'


class ServiceError(Exception):
    """
    服务错误，不应该出现
    """

    def __init__(self, response, code=400):
        super(ServiceError, self).__init__()
        self.response = response
        self.code = code

    def __str__(self):
        return f'ServiceError: {self.response}'
