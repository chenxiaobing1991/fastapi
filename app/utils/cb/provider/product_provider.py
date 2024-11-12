from ..abstract_provider import AbstractProvider

from app.utils.network.response import Response

# 产品引擎包
class ProductProvider(AbstractProvider):

    # 获取产品详情
    def info(self, id)->Response:
        query = f"""
                query MyQuery {{
                  product(id: {id}) {{
                    id
                    creationDate
                    defaultAffiliateId
                    internalCategory
                    price {{
                      id
                      priceType {{
                        id
                        name
                      }}
                      showOriginalAndDiscountPrice
                      availableCurrencies {{
                        name
                      }}
                      priceAbsoluteValues {{
                        quantity
                        value
                        currency {{
                          id
                          name
                        }}
                      }}
                    }}
                    names(languageIds: EN) {{
                      value
                      language {{
                        id
                        name
                        isoCode
                      }}
                    }}
                    bundleProducts {{
                          itemProduct {{
                            id
                            names {{
                              value
                              language {{
                                id
                                name
                                isoCode
                              }}
                            }}
                          }}
                        }}
                  }}
                }}
                """
        response = self.request('/graphql', 'post', query)
        return response

    # 获取产品价格
    def price(self, id)->Response:
        query = f"""
            query MyQuery {{
                  product(id:{id}) {{
                    id
                    price {{
                      id
                      priceType {{
                        id
                        name
                      }}
                      showOriginalAndDiscountPrice
                      availableCurrencies {{
                        name
                      }}
                      priceAbsoluteValues {{
                        quantity
                        value
                        currency {{
                          id
                          name
                        }}
                      }}
                    }}
                    names(languageIds: EN) {{
                      value
                      language {{
                        id
                        name
                      }}
                    }}
                  }}
                }}
           """
        response = self.request('/graphql', 'post', query)
        return response
    #获取产品bundle信息
    def bundle(self,id)->Response:
        query = f"""
                query MyQuery {{
                      product(id: {id}) {{
                        names(languageIds: EN) {{
                          value
                          language {{
                            id
                            name
                          }}
                        }}
                        id
                        bundleProducts {{
                          itemProduct {{
                            id
                            names {{
                              value
                              language {{
                                id
                                name
                                isoCode
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}
                   """
        response = self.request('/graphql', 'post', query)
        return response
