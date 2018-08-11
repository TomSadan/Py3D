class LengthMetaclass(type):

    def __len__(self):
        return self.clslength()

class A(object):
    __metaclass__ = LengthMetaclass

    @classmethod
    def clslength(cls):
        return 7

print len(A)
