from pyckson.const import PYCKSON_SERIALIZER
from pyckson.helpers import is_base_type, get_custom_serializer
from pyckson.providers import ModelProvider
from pyckson.serializers.base import Serializer, BasicSerializer


class GenericSerializer(Serializer):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def serialize(self, obj):
        if is_base_type(obj):
            return BasicSerializer().serialize(obj)
        elif hasattr(obj.__class__, PYCKSON_SERIALIZER):
            return get_custom_serializer(obj.__class__).serialize(obj)
        else:
            return ClassSerializer(self.model_provider).serialize(obj)


class ClassSerializer(Serializer):
    def __init__(self, model_provider: ModelProvider):
        self.model_provider = model_provider

    def serialize(self, obj):
        model = self.model_provider.get_or_build(obj)
        result = {}
        for attribute in model.attributes:
            value = getattr(obj, attribute.python_name, None)
            if value is None and attribute.optional:
                continue
            elif value is None:
                raise ValueError(
                    'attribute {} of {} is None but not marked as optional'.format(attribute.python_name, obj))
            result[attribute.json_name] = attribute.serializer.serialize(value)
        return result


class CustomDeferredSerializer(Serializer):
    def __init__(self, cls):
        self.cls = cls

    def serialize(self, obj):
        return get_custom_serializer(self.cls).serialize(obj)
