class SchemaDefaultOptionsBase:
    pass


class StringDefaultOptions(SchemaDefaultOptionsBase):
    @property
    def min_length(self) -> int:
        return 1

    @property
    def max_length(self) -> int:
        return 10


class RefDefaultOptions(SchemaDefaultOptionsBase):
    pass


class BooleanDefaultOptions(SchemaDefaultOptionsBase):
    pass


class IntegerDefaultOptions(SchemaDefaultOptionsBase):
    pass


class NullDefaultOptions(SchemaDefaultOptionsBase):
    pass


class ObjectDefaultOptions(SchemaDefaultOptionsBase):
    pass


class ArrayDefaultOptions(SchemaDefaultOptionsBase):
    pass


class DefaultOptions:
    def __init__(self):
        self.ref = RefDefaultOptions()
        self.string = StringDefaultOptions()
        self.boolean = BooleanDefaultOptions()
        self.array = ArrayDefaultOptions()
        self.integer = IntegerDefaultOptions()
        self.null = NullDefaultOptions()
        self.object = ObjectDefaultOptions()
