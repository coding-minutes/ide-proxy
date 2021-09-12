def body_validator(serializer_class):
    def decorator(func):
        def wrapped(self, request, **kwargs):
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return func(self,request, validated_data=serializer.data,**kwargs)
        return wrapped
    return decorator
