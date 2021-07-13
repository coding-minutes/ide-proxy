from rest_framework import serializers


class _BaseListSerializer(serializers.ListSerializer):
    @property
    def data(self):
        ret = super().data
        return {"data": ret}


class BaseSerializer(serializers.Serializer):
    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        return _BaseListSerializer(*args, **kwargs)

    @property
    def data(self):
        ret = super().data
        return {"data": ret}
