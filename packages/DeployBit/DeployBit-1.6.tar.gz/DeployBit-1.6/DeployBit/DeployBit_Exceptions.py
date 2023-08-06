class DeployBitError(Exception):
    message = '{content}'
    def __init__(self,content=None,code=None):
        self.content = content
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitLoginError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitDeploymentError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitQueryError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)
        
class DeployBitRetrieveError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitDescribeMetadataError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitListMetadataError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitApexExecuteError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

class DeployBitLogoutError(DeployBitError):
    message = '{content}'
    def __str__(self):
        return self.message.format(content=self.content)

        