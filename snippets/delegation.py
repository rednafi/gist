def delegate(to, *methods):
    def _create_delegator(method):
        def delegator(self, *args, **kwargs):
            obj = getattr(self, to)
            m = getattr(obj, method)
            return m(*args, **kwargs)

        return delegator

    def decortor(klass):
        for method in methods:
            setattr(klass, method, _create_delegator(method))
        return klass

    return decortor


class A:
    def method_a(self, a):
        return a


@delegate("a", "method_a")
class B:
    def __init__(self, a=A()):
        self.a = a


b = B()
print(b.method_a(a=333))
