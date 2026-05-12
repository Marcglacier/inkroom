# app/common/serializers/base.py
class SerializerMixin:

    def to_dict(self):
        raise NotImplementedError("Serializer must implement to_dict()")