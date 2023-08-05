import json


class ConvertAllTo:
    def __init__(self,listt):
        self.listt =listt

    def list_to_dict(self):
        list_dict = [i for i in range(len( self.listt) + 1)]
        return dict(zip(list_dict, self.listt))

    def list_to_json(self,indent: int = 4):
        self.list_to_dict()
        return json.dumps(self.list_to_dict(), indent=indent)

    def convert_to_table(self):
        pass

