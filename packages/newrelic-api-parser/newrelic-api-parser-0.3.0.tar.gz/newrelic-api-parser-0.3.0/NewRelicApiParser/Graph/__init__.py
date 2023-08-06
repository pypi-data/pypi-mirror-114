from NewRelicApiParser.Base import BaseNewRelic
from NewRelicApiParser import Config
from urllib import parse

class GraphQlApi(BaseNewRelic):

    def __init__(self, graphql_key: str):
        super().__init__()
        self.BASE_URI = Config.BASE_GRAPHQL_URI
        self.headers['Api-Key'] = graphql_key

    def query(self, request_body: str) -> dict:
        """
        return the graphql data
        """
        url = self.BASE_URI
        return self.post_data(url, data=request_body)