from dataclasses import dataclass


class PrefixMeta(type):
    def __new__(metacls, cls, bases, classdict):
        try:
            prefix = classdict["Config"].prefix
        except (KeyError, AttributeError):
            prefix = None
        if prefix:
            for attr_name, attr_value in classdict.items():
                conditions = (
                    isinstance(attr_value, str),
                    attr_value != cls,
                    not attr_name.startswith("_"),
                )
                if all(conditions):
                    classdict[attr_name] = prefix + attr_value
        return dataclass((super().__new__(metacls, cls, bases, classdict)))


class Prefix(metaclass=PrefixMeta):
    pass


class Foo(Prefix):
    bar: str = "some_settings"

    class Config:
        prefix = "dev_"


th = Foo()
str(th) == Foo(bar="dev_some_settings")

