from public import public


@public
class Undefined:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __repr__(self):
        return '<undefined>'

    def __bool__(self):
        return False

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __hash__(self):
        return hash(id(self))


undefined = Undefined()
public(undefined=undefined)
