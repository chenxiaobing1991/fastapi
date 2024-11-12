from ..abstract_provider import AbstractProvider
#订单引擎
class OrderProvider(AbstractProvider):
    #订单详情
    def get_info(self,sale_id):
        return self.request(f'/rest/6.0/orders/{sale_id}/','get')
    #订单列表
    def get_list(self,limit=10,page=1,filter={}):
        filter['limit'] = limit
        filter['Page'] = page
        return self.request('/rest/6.0/orders/?'+self.dict_to_query(filter),'get')
