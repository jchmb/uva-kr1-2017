

class SymbolConverter:

    def __init__(self):
        self.map = {}
        self.counter = 1

    def convert(self, symbol):
        if symbol in self.map:
            return self.map[symbol]
        else:
            self.map[symbol] = self.counter
            self.counter += 1
            return self.map[symbol]

    def print_map(self, reverse=False):
        for key, value in self.map.items():
            if reverse:
                print(str(value) + ' -> ' + str(key))
            else:
                print(str(key) + ' -> ' + str(value))


def TestSymbolConverter():
    conv = SymbolConverter()
    p1234 = conv.convert('p1234')
    p1235 = conv.convert('p1235')
    p1234_2 = conv.convert('p1234')
    p1235_2 = conv.convert('p1235')

    assert p1234 == p1234_2 == 1
    assert p1235 == p1235_2 == 2

    conv.print_map()
    conv.print_map(True)

# TestSymbolConverter()
