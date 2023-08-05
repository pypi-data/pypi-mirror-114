class MissingEnvironmentVariableError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__('The ADARA_SDK_CREDENTIALS environment variable does not exist.', *args, **kwargs)
