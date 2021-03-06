class Parser:
    def parse(self, json_value):
        pass


class BasicParser(Parser):
    def parse(self, json_value):
        return json_value


class ListParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser

    def parse(self, json_value):
        return [self.sub_parser.parse(item) for item in json_value]


class SetParser(Parser):
    def __init__(self, sub_parser: Parser):
        self.sub_parser = sub_parser

    def parse(self, json_value):
        return {self.sub_parser.parse(item) for item in json_value}


class DefaultEnumParser(Parser):
    def __init__(self, cls):
        self.cls = cls

    def parse(self, value):
        return self.cls[value]


class CaseInsensitiveEnumParser(Parser):
    def __init__(self, cls):
        self.values = {member.name.lower(): member for member in cls}

    def parse(self, value):
        return self.values[value.lower()]


class DictParser(Parser):
    def parse(self, json_value):
        return json_value
