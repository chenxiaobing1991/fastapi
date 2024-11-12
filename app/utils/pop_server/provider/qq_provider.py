from ..abstract_provider import AbstractProvider
#QQ邮箱
class QQProvider(AbstractProvider):

    def get_uri(self):
        return 'pop.qq.com'