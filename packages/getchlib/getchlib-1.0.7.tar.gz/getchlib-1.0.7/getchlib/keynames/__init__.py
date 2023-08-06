from . import raw
class Key:
    def __init__(self,d):
        self.d=d
    def __eq__(self,e):
        return self.d==e[2:]
for i in dir(raw):
    exec('{}=Key(raw.{})'.format(i,i))
