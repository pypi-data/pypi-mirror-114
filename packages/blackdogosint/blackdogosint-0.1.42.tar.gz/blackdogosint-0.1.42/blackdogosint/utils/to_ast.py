import ast


class TOAST:
    def __init__(self, dado):
        self.dado = None

    def literal_eval(self):
        return ast.literal_eval(self.dado)

