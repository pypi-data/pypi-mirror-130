from outer.VirtualTerminal import VirtualTerminal
from outer.Object import File, Dir, Object
import os


class BluePrint(Dir):
    def __init__(self, root_dir='log', key:str = None):
        self.path = os.path.join(root_dir, key) if key is not None else root_dir
        super(BluePrint, self).__init__(path='')
        # default to init
        self.terminal = VirtualTerminal(root=root_dir, key=key)
        self.set_terminal(self.terminal)

    def init(self):
        # set terminal
        for name, obj in vars(self).items():
            if type(obj) is Object or issubclass(type(obj), Object):
                obj.set_terminal(self.terminal)
        return self
