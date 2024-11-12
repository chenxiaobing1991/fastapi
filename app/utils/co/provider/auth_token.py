import time
from ..abstract_provider import AbstractProvider
from datetime import datetime
import hmac
import hashlib
class AuthToken(AbstractProvider):

    #获取hash值
    def get_hash(self,formatted_utc_now:str)->str:
        hash_str = str(len(self.get_config().get_merchant_code())) + self.get_config().get_merchant_code() + str(len(formatted_utc_now)) + formatted_utc_now
        secret_key=self.get_config().get_secret_key()
        hash_value = hmac.new(secret_key.encode(), hash_str.encode(), hashlib.sha256).hexdigest()
        return hash_value
    #获取授权令牌
    def get_access_token(self):
        utc_now = datetime.utcnow()
        formatted_utc_now = utc_now.strftime('%Y-%m-%d %H:%M:%S')
        merchant_code=self.get_config().get_merchant_code()
        hash_value=self.get_hash(formatted_utc_now)
        return f'code="{merchant_code}" date="{formatted_utc_now}" hash="{hash_value}" algo="sha256"'
