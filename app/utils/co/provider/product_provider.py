from ..abstract_provider import AbstractProvider
#产品管理
class ProductProvider(AbstractProvider):

    #获取产品列表
    def get_list(self,limit=10,page=1,filter={}):
        filter['limit']=limit
        filter['Page'] = page
        return self.request('/rest/6.0/products/?'+self.dict_to_query(filter),'get')


    #产品名称
    def get_info(self,product_code:str):
        return self.request(f'/rest/6.0/products/{product_code}/', 'get')

