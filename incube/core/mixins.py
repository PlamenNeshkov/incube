from rest_framework import mixins

class ImmutableModelMixin(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin):
    pass
