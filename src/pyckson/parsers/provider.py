from enum import Enum
from typing import List, _ForwardRef, Dict, Set

from pyckson.const import BASIC_TYPES, PYCKSON_TYPEINFO, PYCKSON_ENUM_OPTIONS, ENUM_CASE_INSENSITIVE, PYCKSON_PARSER
from pyckson.helpers import TypeProvider
from pyckson.parsers.advanced import UnresolvedParser, ClassParser, CustomDeferredParser
from pyckson.parsers.base import Parser, BasicParser, ListParser, CaseInsensitiveEnumParser, DefaultEnumParser, \
    DictParser, SetParser
from pyckson.providers import ParserProvider, ModelProvider


class ParserProviderImpl(ParserProvider):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def get(self, obj_type, parent_class, name_in_parent) -> Parser:
        if obj_type in BASIC_TYPES:
            return BasicParser()
        if hasattr(obj_type, PYCKSON_PARSER):
            return CustomDeferredParser(obj_type)
        if type(obj_type) is str or type(obj_type) is _ForwardRef:
            return UnresolvedParser(TypeProvider(parent_class, obj_type), self.model_provider)
        if obj_type is list:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return ListParser(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('list parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                      parent_class.__name__))
        if obj_type is set:
            type_info = getattr(parent_class, PYCKSON_TYPEINFO, dict())
            if name_in_parent in type_info:
                sub_type = type_info[name_in_parent]
                return SetParser(self.get(sub_type, parent_class, name_in_parent))
            else:
                raise TypeError('set parameter {} in class {} has no subType'.format(name_in_parent,
                                                                                      parent_class.__name__))
        if issubclass(obj_type, List):
            return ListParser(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if issubclass(obj_type, Set):
            return SetParser(self.get(obj_type.__args__[0], parent_class, name_in_parent))
        if issubclass(obj_type, Enum):
            options = getattr(obj_type, PYCKSON_ENUM_OPTIONS, {})
            if options.get(ENUM_CASE_INSENSITIVE, False):
                return CaseInsensitiveEnumParser(obj_type)
            else:
                return DefaultEnumParser(obj_type)
        if issubclass(obj_type, Dict) or issubclass(obj_type, dict):
            return DictParser()
        return ClassParser(obj_type, self.model_provider)
