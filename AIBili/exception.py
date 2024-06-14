class RequestFailedException(Exception):
    def __init__(self, message="请求失败，已达到最大重试次数"):
        self.message = message
        super().__init__(self.message)


class VerificationRiskException(Exception):
    def __init__(self, message="风控校验失败"):
        self.message = message
        super().__init__(self.message)


class AuthorityInsufficientException(Exception):
    def __init__(self, message="访问权限不足"):
        self.message = message
        super().__init__(self.message)
