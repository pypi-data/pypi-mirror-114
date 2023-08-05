from blackdogosint.utils.exception.exception import MissingKey
from blackdogosint.utils.coreosint import useragentrandom


class SearchBinaryEdge:

    def __init__(self, word, limit):
        self.word = word
        self.totalhosts = set()
        self.proxy = False
        self.key = 'df15598c-e782-41a4-83a2-96f34878078c'
        self.limit = min(limit, 501)
        self.limit = 2 if self.limit == 1 else self.limit
        if self.key is None:
            raise MissingKey('binaryedge')

    async def do_search(self):
        base_url = f'https://api.binaryedge.io/v2/query/domains/subdomain/{self.word}'
        headers = {'X-KEY': self.key, 'User-Agent':useragentrandom()}
        for page in range(1, self.limit):
            params = {'page': page}
            response = await AsyncFetcher.fetch_all([base_url], json=True, proxy=self.proxy, params=params, headers=headers)
            responses = response[0]
            dct = responses
            if ('status' in dct.keys() and 'message' in dct.keys()) and \
                    (dct['status'] == 400 or 'Bad Parameter' in dct['message'] or 'Error' in dct['message']):
                # 400 status code means no more results
                break
            if 'events' in dct.keys():
                if len(dct['events']) == 0:
                    break
                self.totalhosts.update({host for host in dct['events']})
            await asyncio.sleep(get_delay())

    async def get_hostnames(self) -> set:
        return self.totalhosts

    async def process(self, proxy=False):
        self.proxy = proxy
        await self.do_search()
